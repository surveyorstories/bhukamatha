# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Item Gui Registry
Description          : Registers GUI metadata for QR and barcode items.
Date                 : 10-08-2020
copyright            : (C) 2020 by John Gitau
email                : gkahiu@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QCoreApplication
from qgis.gui import (
    QgsGui,
    QgsLayoutItemAbstractGuiMetadata,
    QgsLayoutItemGuiGroup
)
from bhu_kamatha.layout.qrcode_item import (
    QR_CODE_TYPE,
    QrCodeLayoutItem
)
from bhu_kamatha.layout.linear_barcode_item import (
    LINEAR_BARCODE_TYPE,
    LinearBarcodeLayoutItem
)
from bhu_kamatha.utils import (
    get_icon
)
from bhu_kamatha.gui.qrcode_widget import QrCodeLayoutItemWidget
from bhu_kamatha.gui.linear_barcode_widget import \
    LinearBarcodeLayoutItemWidget

ITEM_CATEGORY = 'qrbarcodeitem'


class QrCodeLayoutItemGuiMetadata(QgsLayoutItemAbstractGuiMetadata):
    """Stores GUI metadata for a QR code layout item."""

    def __init__(self):
        super().__init__(
            QR_CODE_TYPE,
            QCoreApplication.translate('QrBarCodeLayoutItem', 'QR Code'),
            ITEM_CATEGORY
        )

    def createItemWidget(self, item):  # pylint: disable=missing-function-docstring, no-self-use
        return QrCodeLayoutItemWidget(None, item)

    def createItem(self, layout):  # pylint: disable=missing-function-docstring, no-self-use
        return QrCodeLayoutItem(layout)

    def creationIcon(self):  # pylint: disable=missing-function-docstring, no-self-use
        return get_icon('qrcode_plus.svg')


class LinearBarcodeLayoutItemGuiMetadata(QgsLayoutItemAbstractGuiMetadata):
    """Stores GUI metadata for a linear barcode layout item."""

    def __init__(self):
        super().__init__(
            LINEAR_BARCODE_TYPE,
            QCoreApplication.translate(
                'QrBarCodeLayoutItem',
                'Linear Barcode'
            ),
            ITEM_CATEGORY
        )

    def createItemWidget(self, item):  # pylint: disable=missing-function-docstring, no-self-use
        return LinearBarcodeLayoutItemWidget(None, item)

    def createItem(self, layout):  # pylint: disable=missing-function-docstring, no-self-use
        return LinearBarcodeLayoutItem(layout)

    def creationIcon(self):  # pylint: disable=missing-function-docstring, no-self-use
        return get_icon('barcode_plus.svg')


def register_items_gui_metadata():
    """Registers GUI metadata for QR and barcode items."""
    item_registry = QgsGui.layoutItemGuiRegistry()

    # Create menu group
    item_registry.addItemGroup(
        QgsLayoutItemGuiGroup(
            ITEM_CATEGORY,
            QCoreApplication.translate('QrBarCodeLayoutItem', 'Barcode Item'),
            get_icon('qr_barcode.svg')
        )
    )

    # Add linear barcode gui metadata
    linear_barcode_meta = LinearBarcodeLayoutItemGuiMetadata()
    item_registry.addLayoutItemGuiMetadata(linear_barcode_meta)

    # Add QR code gui metadata
    qr_code_meta = QrCodeLayoutItemGuiMetadata()
    item_registry.addLayoutItemGuiMetadata(qr_code_meta)
