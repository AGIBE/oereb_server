# -*- coding: utf-8 -*-
from pyramid_oereb.contrib.print_proxy.mapfish_print.mapfish_print import Renderer

class BERenderer(Renderer):
    
    def convert_to_printable_extract(self, extract_dict, feature_geometry):
        ed = super(BERenderer, self).convert_to_printable_extract(extract_dict, feature_geometry)

        # Die Darstellungsreihenfolge auf den plr-Seiten ist für den Kanton
        # Bern ungünstig. Wir möchten den AV-WMS über dem PLR-WMS legen. Die
        # Reihenfolge muss daher im print_proxy übersteuert werden.

        for plr in ed['RealEstate_RestrictionOnLandownership']:
            plr['baseLayers']['layers'].reverse()

        return ed

