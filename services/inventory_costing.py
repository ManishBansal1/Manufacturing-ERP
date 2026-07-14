from models import InventoryLedger
from models import ItemMaster
from models import ProductionEntryDetail
from models import db


def update_inventory_cost(item_id):

    ledger = (
        InventoryLedger.query
        .filter_by(
            item_id=item_id
        )
        .order_by(
            InventoryLedger.trans_date,
            InventoryLedger.id
        )
        .all()
    )

    running_qty = 0
    running_value = 0

    for row in ledger:


        if row.qty_in > 0:

            # Opening Stock / Purchase etc.
            if row.reference_type != "PRODUCTION":

                if row.value_in is None:
                    row.value_in = 0

                row.unit_cost = (
                    row.value_in / row.qty_in
                    if row.qty_in > 0
                    else 0
                )

            else:

                production_inputs = (
                    ProductionEntryDetail.query
                    .filter_by(
                        production_entry_id=row.reference_id,
                        transaction_type="INPUT"
                    )
                    .all()
                )

                production_cost = 0

                for input_row in production_inputs:

                    issue = (
                        InventoryLedger.query
                        .filter_by(
                            reference_type="PRODUCTION",
                            reference_id=row.reference_id,
                            item_id=input_row.item_id
                        )
                        .first()
                    )

                    if issue:

                        production_cost += (issue.value_out or 0)

                row.value_in = production_cost or 0

                row.unit_cost = (
                    production_cost / row.qty_in
                    if row.qty_in > 0
                    else 0
                )

            running_qty += (row.qty_in or 0)

            running_value += (row.value_in or 0)

        elif row.qty_out > 0:

            if running_qty > 0:

                avg = (
                    running_value / running_qty
                    if running_qty > 0
                    else 0
                )

            else:

                avg = 0

            row.unit_cost = avg

            row.value_out = row.qty_out * avg

            running_qty -= (row.qty_out or 0)

            running_value -= (row.value_out or 0)

        row.running_qty = running_qty

        row.running_value = running_value

        if running_qty > 0:

            row.weighted_average_rate = (
                running_value / running_qty
            )

        else:

            row.weighted_average_rate = 0

    db.session.commit()


def rebuild_inventory():

    items = ItemMaster.query.order_by(
        ItemMaster.item_code
    ).all()

    for item in items:

        update_inventory_cost(item.id)