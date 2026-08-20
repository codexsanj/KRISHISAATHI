"""
Farm Profit Engine

Calculates total recorded expenses, total sales revenue, gross return, and net profit per crop cycle or farm.
"""

from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.all_models import ExpenseRecord, SaleRecord, FarmActivity, CropCycle

class FarmProfitEngine:
    @staticmethod
    def compute_farm_profit(db: Session, farmer_id: int, crop_cycle_id: int = None) -> Dict[str, Any]:
        # Expenses query
        exp_query = db.query(ExpenseRecord).filter(ExpenseRecord.farmer_id == farmer_id)
        if crop_cycle_id:
            exp_query = exp_query.filter(ExpenseRecord.crop_cycle_id == crop_cycle_id)
        expenses = exp_query.all()

        # Activities cost query
        act_query = db.query(FarmActivity).filter(FarmActivity.farmer_id == farmer_id)
        if crop_cycle_id:
            act_query = act_query.filter(FarmActivity.crop_cycle_id == crop_cycle_id)
        activities = act_query.all()

        # Sales query
        sale_query = db.query(SaleRecord).filter(SaleRecord.farmer_id == farmer_id)
        if crop_cycle_id:
            sale_query = sale_query.filter(SaleRecord.crop_cycle_id == crop_cycle_id)
        sales = sale_query.all()

        # Calculate totals
        total_exp_records = sum(e.amount for e in expenses)
        total_act_costs = sum(a.cost for a in activities if a.cost)
        total_recorded_cost = total_exp_records + total_act_costs

        total_revenue = sum(s.net_revenue for s in sales)
        gross_return = total_revenue
        net_profit = total_revenue - total_recorded_cost

        # Categorize expenses
        breakdown = {
            "SEED": 0.0, "FERTILIZER": 0.0, "PESTICIDE": 0.0,
            "LABOUR": 0.0, "IRRIGATION": 0.0, "EQUIPMENT": 0.0,
            "TRANSPORT": 0.0, "OTHER": 0.0
        }
        for e in expenses:
            cat = (e.category or "OTHER").upper()
            if cat in breakdown:
                breakdown[cat] += e.amount
            else:
                breakdown["OTHER"] += e.amount

        # Get crop name
        crop_name = "Overall Farm"
        if crop_cycle_id:
            cc = db.query(CropCycle).filter(CropCycle.id == crop_cycle_id).first()
            if cc:
                crop_name = cc.crop_name

        return {
            "farmer_id": farmer_id,
            "crop_cycle_id": crop_cycle_id,
            "crop_name": crop_name,
            "total_recorded_cost": round(total_recorded_cost, 2),
            "total_revenue": round(total_revenue, 2),
            "gross_return": round(gross_return, 2),
            "net_profit": round(net_profit, 2),
            "expense_breakdown": breakdown,
            "is_estimated": len(expenses) == 0 and len(sales) == 0
        }

farm_profit_engine = FarmProfitEngine()
