# -*- coding: utf-8 -*-
from pyramid_oereb.contrib.print_proxy.mapfish_print import Renderer

class BERenderer(Renderer):
    
    def convert_to_printable_extract(self, extract_dict, feature_geometry, pdf_to_join):
        ed = super(BERenderer, self).convert_to_printable_extract(extract_dict, feature_geometry, pdf_to_join)

        # Der Map-Parameter des Mapservers geht im PrintProxy verloren.
        # Er wird hier hardcoded eingefügt.

        # Zunächst für die einzelnen ÖREB-Seiten
        for plr in ed['RealEstate_RestrictionOnLandownership']:
            for lyr in plr['baseLayers']['layers']:
                if 'geodb.mopube_bbf' in lyr['layers']:
                    lyr['customParams']['map'] = 'oerebav_de'
                else:
                    lyr['customParams']['map'] = 'oereb_de'
        

        # Und hier noch für die Titelseite
        for lyr in ed['baseLayers']['layers']:
            if 'geodb.mopube_bbf' in lyr['layers']:
                lyr['customParams']['map'] = 'oerebav_de'
            else:
                lyr['customParams']['map'] = 'oereb_de'

        return ed

