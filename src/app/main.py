from __future__ import annotations

from datetime import date, timedelta
from typing import List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl


app = FastAPI(title="Travel Maker API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeUrlRequest(BaseModel):
    url: HttpUrl
    start_date: Optional[date] = None
    days: int = 3


class PlaceInfo(BaseModel):
    name: str
    category: str
    open_time: str
    close_time: str
    fee_krw: int


class DayPlan(BaseModel):
    day: int
    date: Optional[date]
    places: List[PlaceInfo]


class ItinerarySkeleton(BaseModel):
    title: str
    days: int
    plans: List[DayPlan]


class AnalyzeUrlResponse(BaseModel):
    source_url: HttpUrl
    summary: str
    itinerary: ItinerarySkeleton


class OptimizeRouteRequest(BaseModel):
    places: List[str]


class OptimizeRouteResponse(BaseModel):
    ordered_places: List[str]
    note: str


class TripCreateRequest(BaseModel):
    itinerary: ItinerarySkeleton


class TripResponse(BaseModel):
    id: str
    itinerary: ItinerarySkeleton


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


_TRIPS: dict[str, ItinerarySkeleton] = {}


def _build_dummy_places(day_index: int) -> List[PlaceInfo]:
    base_fees = [0, 12000, 18000]
    return [
        PlaceInfo(
            name=f"샘플 장소 {day_index}-1",
            category="명소",
            open_time="09:00",
            close_time="18:00",
            fee_krw=base_fees[day_index % len(base_fees)],
        ),
        PlaceInfo(
            name=f"샘플 장소 {day_index}-2",
            category="맛집",
            open_time="11:00",
            close_time="22:00",
            fee_krw=0,
        ),
    ]


def _build_itinerary(days: int, start: Optional[date]) -> ItinerarySkeleton:
    plans: List[DayPlan] = []
    for i in range(days):
        plan_date = start + timedelta(days=i) if start else None
        plans.append(
            DayPlan(day=i + 1, date=plan_date, places=_build_dummy_places(i + 1))
        )
    return ItinerarySkeleton(title="여행 일정 뼈대", days=days, plans=plans)


@app.post("/analyze-url", response_model=AnalyzeUrlResponse)
def analyze_url(payload: AnalyzeUrlRequest) -> AnalyzeUrlResponse:
    itinerary = _build_itinerary(payload.days, payload.start_date)
    return AnalyzeUrlResponse(
        source_url=payload.url,
        summary="입력된 URL 내용을 기반으로 일정 뼈대를 생성. (더미 응답)",
        itinerary=itinerary
    )


@app.post("/optimize-route", response_model=OptimizeRouteResponse)
def optimize_route(payload: OptimizeRouteRequest) -> OptimizeRouteResponse:
    if len(payload.places) <= 2:
        ordered = payload.places
    else:
        ordered = [payload.places[0]] + sorted(payload.places[1:])
    return OptimizeRouteResponse(
        ordered_places=ordered,
        note="현재는 더미 최적화 로직. (거리/시간 기반 알고리즘 추가 예정)",
    )


@app.post("/trips", response_model=TripResponse)
def create_trip(payload: TripCreateRequest) -> TripResponse:
    trip_id = uuid4().hex
    _TRIPS[trip_id] = payload.itinerary
    return TripResponse(id=trip_id, itinerary=payload.itinerary)


@app.get("/trips", response_model=List[TripResponse])
def list_trips() -> List[TripResponse]:
    return [TripResponse(id=trip_id, itinerary=data) for trip_id, data in _TRIPS.items()]


@app.get("/trips/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: str) -> TripResponse:
    itinerary = _TRIPS.get(trip_id)
    if not itinerary:
        raise HTTPException(status_code=404, detail="Trip not found")
    return TripResponse(id=trip_id, itinerary=itinerary)


@app.put("/trips/{trip_id}", response_model=TripResponse)
def update_trip(trip_id: str, payload: TripCreateRequest) -> TripResponse:
    if trip_id not in _TRIPS:
        raise HTTPException(status_code=404, detail="Trip not found")
    _TRIPS[trip_id] = payload.itinerary
    return TripResponse(id=trip_id, itinerary=payload.itinerary)


@app.delete("/trips/{trip_id}")
def delete_trip(trip_id: str) -> dict:
    if trip_id not in _TRIPS:
        raise HTTPException(status_code=404, detail="Trip not found")
    del _TRIPS[trip_id]
    return {"deleted": True}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, app_dir="src")
