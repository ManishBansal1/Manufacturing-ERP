from flask import (
    render_template,
    request,
    redirect,
    url_for,
    jsonify
)

from flask_login import (
    login_required
)

from . import sales_bp

from models import (
    db,
    SalesInvoiceHeader,
    SalesInvoiceDetail,
    CustomerPOHeader,
    CustomerPODetail,
    CustomerMaster,
    DestinationMaster,
    TransporterMaster,
    ItemMaster,
    InventoryLedger
)

print("Sales routes loaded")

@sales_bp.route(
    "/invoice/get-po-details/<int:po_id>"
)
@login_required
def get_po_details(po_id):

    po = CustomerPOHeader.query.get_or_404(po_id)

    result = {
        "customer": po.customer.customer_name,
        "lines": []
    }

    for line in po.details:

        inventory = InventoryLedger.query.filter_by(
            item_id=line.item_id
        ).first()

        available_qty = (
        db.session.query(
        db.func.sum(
            InventoryLedger.qty_in -
            InventoryLedger.qty_out
        )
        )
        .filter(
        InventoryLedger.item_id == line.item_id
        )
        .scalar()
        or 0
        )

        result["lines"].append({

            "po_detail_id": line.id,

            "item_name": line.item.item_name,

            "ordered_qty": line.qty,

            "already_dispatched": line.dispatched_qty,

            "pending_qty": line.pending_qty,

            "available_qty": available_qty,

            "rate": line.rate,

            "freight": line.freight,

            "gst_rate": line.gst_rate

        })

    return jsonify(result)

