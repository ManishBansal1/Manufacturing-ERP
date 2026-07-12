from flask import Blueprint, render_template
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

    if today.month >= 4:
        current_fy = today.year + 1
    else:
        current_fy = today.year

    financial_years = []

    for fy in range(current_fy, current_fy - 6, -1):
        financial_years.append(fy)

    invoices = (
        SalesInvoiceHeader.query
        .order_by(SalesInvoiceHeader.invoice_date.desc())
        .all()
    )

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

            "payment_status":
                payment.status if payment else ""

        })

    return render_template(

        "outstanding_receipts_dashboard.html",

        financial_years=financial_years,

        current_fy=current_fy,

        receivable_rows=receivable_rows

    )