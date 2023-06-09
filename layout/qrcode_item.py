# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : LayoutItemQrCode
Description          : QR code item for use in QGIS print layout
Date                 : 04-08-2020
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
from qgis.PyQt.QtCore import (
    QCoreApplication
)
from qgis.core import (
    QgsLayoutItemAbstractMetadata,
    QgsLayoutItemRegistry
)

from bhu_kamatha.extlibs import segno
from bhu_kamatha.layout.abstract_barcode import (
    AbstractBarcodeLayoutItem,
    BarcodeException
)
from bhu_kamatha.utils import (
    get_icon
)

QR_CODE_TYPE = QgsLayoutItemRegistry.PluginItem + 2345


class QrCodeLayoutItem(AbstractBarcodeLayoutItem):
    """Item for rendering quick response code."""

    _ATTR_MICRO = 'isMicro'
    _ATTR_BG_COLOR = 'codeBackgroundColor'
    _ATTR_DATA_COLOR = 'dataColor'
    _DEF_BG_COLOR = '#FFFFFF'
    _DEF_DATA_COLOR = '#000000'

    def __init__(self, *args):
        super().__init__(*args)
        self._is_micro = False
        self._bg_color = self._DEF_BG_COLOR
        self._data_color = self._DEF_DATA_COLOR
        self._scale = 10

    @property
    def is_micro(self):
        """
        :return: Returns True if micro QR code or standard QR code.
        :rtype: bool
        """
        return self._is_micro

    @is_micro.setter
    def is_micro(self, qrc_type):
        """
        Sets the type of the QR code.
        :param qrc_type: True if the code should be a micro QR code, else
        False if its a standard QR code.
        :type qrc_type: bool
        """
        if self._is_micro != qrc_type:
            self._is_micro = qrc_type
            self.update_item()

    @property
    def bg_color(self):
        """
        :return: Returns the background color code.
        :rtype: str
        """
        return self._bg_color

    @bg_color.setter
    def bg_color(self, clr):
        """
        Sets the color code of the QR code background.
        :param clr: Background color code.
        :type clr: str
        """
        if self._bg_color != clr:
            self._bg_color = clr
            self.update_item()

    @property
    def data_color(self):
        """
        :return: Returns the color code of the data blocks.
        :rtype: str
        """
        return self._data_color

    @data_color.setter
    def data_color(self, clr):
        """
        Sets the color code of the data blocks.
        :param clr: Data blocks color code.
        :type clr: str
        """
        if self._data_color != clr:
            self._data_color = clr
            self.update_item()

    def icon(self):  # pylint: disable=no-self-use
        """Return item's icon."""
        return get_icon('qrcode.svg')

    def _gen_image(self, file_path):
        """Generate QR Code based on the computed value."""
        try:
            qr = segno.make(
                self.computed_value(),
                micro=self._is_micro
            )
            # Use options for compressing the output file
            qr.save(
                file_path,
                scale=self._scale,
                dark=self._data_color,
                light=self._bg_color,
                border=1,
                xmldecl=False,
                svgns=False,
                nl=False
            )
        except segno.DataOverflowError as doe:
            raise BarcodeException(
                'Data too large, change to standard QR code.'
            ) from doe
        except ValueError as ve:
            raise BarcodeException(str(ve)) from ve

    def type(self):  # pylint: disable=no-self-use
        """Return item's unique identifier."""
        return QR_CODE_TYPE

    def _write_props_to_el(self, el, document, context):
        """Write attributes to document."""
        el.setAttribute(self._ATTR_MICRO, str(self._is_micro))
        el.setAttribute(self._ATTR_BG_COLOR, str(self._bg_color))
        el.setAttribute(self._ATTR_DATA_COLOR, str(self._data_color))

        return True

    def _read_props_from_el(self, el, document, context):
        """Reads item attributes."""
        self._is_micro = self._str_to_bool(
            el.attribute(self._ATTR_MICRO, 'False')
        )
        self._bg_color = str(
            el.attribute(self._ATTR_BG_COLOR, self._DEF_BG_COLOR)
        )
        self._data_color = str(
            el.attribute(self._ATTR_DATA_COLOR, self._DEF_DATA_COLOR)
        )
        self.update_item()

        return True


# pylint: disable=too-few-public-methods
class QrCodeLayoutItemMetadata(QgsLayoutItemAbstractMetadata):
    """Metadata info of the QR code item."""

    def __init__(self):
        super().__init__(
            QR_CODE_TYPE,
            QCoreApplication.translate('QrBarCodeLayoutItem', 'QR Code')
        )

    def createItem(self, layout):  # pylint: disable=no-self-use
        """Factory method that return the QR Code Item."""
        return QrCodeLayoutItem(layout)
