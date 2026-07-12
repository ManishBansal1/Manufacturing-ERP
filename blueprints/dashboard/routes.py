from flask import Blueprint, render_template, request
from flask_login import login_required

from datetime import date

from sqlalchemy import func

from sqlalchemy import and_

from models import (

    CustomerPOHeader,
    CustomerPODetail,
    DestinationMaster,
    SalesInvoiceHeader,
    SalesInvoiceDetail,
    ReceivingNoteHeader,
    ReceivingNoteDetail,
    BillSubmissionHeader,
    BillSubmissionDetail,
    PaymentReceiptHeader,
    CustomerMaster,
    ItemMaster,
    db

)

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html"
    )

@dashboard_bp.route("/dashboard/outstanding-receipts")
@login_required
def outstanding_receipts_dashboard():

    today = date.today()

    selected_fy = request.args.get(
    "financial_year",
    type=int
    )

    if not selected_fy:

        if today.month >= 4:

            selected_fy = today.year + 1

        else:

            selected_fy = today.year

    if today.month >= 4:
        current_fy = today.year + 1
    else:
        current_fy = today.year

    financial_years = []

    for fy in range(current_fy, current_fy - 6, -1):
        financial_years.append(fy)

    query = SalesInvoiceHeader.query.filter(

    SalesInvoiceHeader.status != "CANCELLED"

    )

    fy_start = date(

    selected_fy - 1,

    4,

    1

    )

    fy_end = date(

        selected_fy,

        3,

        31

    )

    from_date = request.args.get("from_date")

    if from_date:

        from_date = date.fromisoformat(from_date)

    to_date = request.args.get("to_date")

    if to_date:

        to_date = date.fromisoformat(to_date)

    invoice_status = request.args.get("invoice_status")

    item_name = request.args.get("item_name")

    customer_name = request.args.get("customer_name")

    query = query.filter(

        SalesInvoiceHeader.invoice_date >= fy_start,

        SalesInvoiceHeader.invoice_date <= fy_end

    )

    if from_date:

        query = query.filter(

            SalesInvoiceHeader.invoice_date >= from_date

        )

    if to_date:

        query = query.filter(

            SalesInvoiceHeader.invoice_date <= to_date

        )

    if invoice_status and invoice_status != "ALL":

        query = query.filter(

            SalesInvoiceHeader.status == invoice_status

        )

    if item_name and item_name != "ALL":

        query = query.join(

            SalesInvoiceDetail

        ).join(

            ItemMaster

        ).filter(

            ItemMaster.item_name == item_name

        )

    
    if customer_name and customer_name != "ALL":

        query = query.join(

            CustomerMaster

        ).filter(

            CustomerMaster.customer_name == customer_name

        )

    customer_list = (

        CustomerMaster.query

        .order_by(

            CustomerMaster.customer_name

        )

        .all()

    )



    invoices = query.order_by(

    SalesInvoiceHeader.invoice_date.desc()

    ).all()

    ''' invoices = (
        SalesInvoiceHeader.query
        .filter(SalesInvoiceHeader.status != "CANCELLED")
        .order_by(SalesInvoiceHeader.invoice_date.desc())
        .all()
    )'''

    receivable_rows = []

    for invoice in invoices:

        dispatch_qty = (
            db.session.query(
                func.sum(SalesInvoiceDetail.dispatch_qty)
            )
            .filter(
                SalesInvoiceDetail.sales_invoice_header_id == invoice.id
            )
            .scalar()
            or 0
        )

        item_names = (
            db.session.query(SalesInvoiceDetail)
            .filter(
                SalesInvoiceDetail.sales_invoice_header_id == invoice.id
            )
            .all()
        )

        item_name = ", ".join(
            sorted({
            detail.item.item_name
            for detail in item_names})
        )

        rnote = (
            ReceivingNoteHeader.query
            .filter(
                ReceivingNoteHeader.sales_invoice_header_id == invoice.id,
                ReceivingNoteHeader.status != "Cancelled"
            )
            .order_by(
                ReceivingNoteHeader.id.desc()
            )
            .first()
        )

        if rnote:

            received_qty = (
                db.session.query(
                    func.sum(ReceivingNoteDetail.received_qty)
                )
                .filter(
                    ReceivingNoteDetail.receiving_note_header_id == rnote.id
                )
                .scalar()
                or 0
            )

        else:

            received_qty = 0

        bill = (
            BillSubmissionHeader.query
            .filter(
                BillSubmissionHeader.sales_invoice_header_id == invoice.id,
                BillSubmissionHeader.status != "Cancelled"
            )
            .order_by(
                BillSubmissionHeader.id.desc()
            )
            .first()
        )

        payment = None

        if bill:

            payment = (
                PaymentReceiptHeader.query
                .filter(
                    PaymentReceiptHeader.bill_submission_header_id == bill.id,
                    PaymentReceiptHeader.status == "ACTIVE"
                )
                .first()
            )

        pending_amount = (
            (bill.bill_amount if bill else 0)
            -
            (payment.amount_received if payment else 0)
            -
            (payment.tds_deducted if payment else 0)
            -
            (payment.ld_charges if payment else 0)
            -
            (payment.general_damage_charges if payment else 0)
            -
            (payment.other_deductions if payment else 0)
        )

        if invoice.status == "Payment Received" and payment:

            collection_days = (
                payment.payment_date - invoice.invoice_date
            ).days

        else:

            collection_days = (
                today - invoice.invoice_date
            ).days

        receivable_rows.append({

            "customer_po_no":
                invoice.customer_po.customer_po_no,

            "item_name":
                item_name,

            "customer_name":
                invoice.customer.customer_name,

            "destination_name":
                invoice.destination.destination_name,

            "dispatch_qty":
                dispatch_qty,

            "received_qty":
                received_qty,

            "invoice_no":
                invoice.invoice_no,

            "invoice_date":
                invoice.invoice_date,

            "invoice_status":
                invoice.status,

            "rnote_no":
                rnote.rnote_no if rnote else "",

            "rnote_date":
                rnote.rnote_date if rnote else None,

            "bill_submission_no":
                bill.bill_submission_no if bill else "",

            "bill_submission_date":
                bill.bill_submission_date if bill else None,

            "bill_amount":
                bill.bill_amount if bill else 0,

            "payment_date":
                payment.payment_date if payment else None,

            "amount_received":
                payment.amount_received if payment else 0,

            "tds_deducted":
                payment.tds_deducted if payment else 0,

            "ld_charges":
                payment.ld_charges if payment else 0,

            "general_damage_charges":
                payment.general_damage_charges if payment else 0,

            "other_deductions":
                payment.other_deductions if payment else 0,

            "pending_amount":
                pending_amount,

            "collection_days":
                collection_days,

            "payment_status":
                payment.status if payment else ""

        })

    grand_totals = {

        "dispatch_qty": 0,

        "received_qty": 0,

        "bill_amount": 0,

        "amount_received": 0,

        "tds": 0,

        "ld": 0,

        "general_damage": 0,

        "other_deductions": 0,

        "pending_amount": 0

    }

    for row in receivable_rows:

        grand_totals["dispatch_qty"] += row["dispatch_qty"]

        grand_totals["received_qty"] += row["received_qty"]

        grand_totals["bill_amount"] += row["bill_amount"]

        grand_totals["amount_received"] += row["amount_received"]

        grand_totals["tds"] += row["tds_deducted"]

        grand_totals["ld"] += row["ld_charges"]

        grand_totals["general_damage"] += row["general_damage_charges"]

        grand_totals["other_deductions"] += row["other_deductions"]

        grand_totals["pending_amount"] += row["pending_amount"]

    item_list = (

        db.session.query(

            ItemMaster.item_name

        )

        .join(
            SalesInvoiceDetail,

            SalesInvoiceDetail.item_id == ItemMaster.id

        )

        .filter(
            ItemMaster.item_type == "Finished Goods"

        )

        .distinct()

        .order_by(

            ItemMaster.item_name

        )

        .all()

    )


    summary = {

        "outstanding_amount": 0,

        "pending_bills": 0,

        "average_collection_days": 0,

        "oldest_outstanding": 0

    }

    payment_days_total = 0

    payment_invoice_count = 0

    for row in receivable_rows:

        # Outstanding Amount
        summary["outstanding_amount"] += row["pending_amount"]

        # Bills Pending
        if row["invoice_status"] not in (

            "Payment Received",

            "Cancelled"

        ):

            summary["pending_bills"] += 1

        # Average Collection Days
        if row["invoice_status"] == "Payment Received":

            payment_days_total += row["collection_days"]

            payment_invoice_count += 1

        # Oldest Outstanding
        if row["invoice_status"] not in (

            "Payment Received",

            "Cancelled"

        ):

            if row["collection_days"] > summary["oldest_outstanding"]:

                summary["oldest_outstanding"] = row["collection_days"]

    if payment_invoice_count:

        summary["average_collection_days"] = round(

            payment_days_total /

            payment_invoice_count,

            1

        )

    else:

        summary["average_collection_days"] = 0


    return render_template(

        "outstanding_receipts_dashboard.html",

        financial_years=financial_years,

        selected_fy=selected_fy,

        from_date=from_date,

        to_date=to_date,

        invoice_status=invoice_status,

        item_list=item_list,

        item_name=item_name,

        customer_list=customer_list,

        customer_name=customer_name,

        receivable_rows=receivable_rows,

        grand_totals=grand_totals,
        
        summary=summary

    )