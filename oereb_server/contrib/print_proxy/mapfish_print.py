# -*- coding: utf-8 -*-
from pyramid_oereb.contrib.print_proxy.mapfish_print import Renderer

class BERenderer(Renderer):
    
    def convert_to_printable_extract(self, extract_dict, feature_geometry, pdf_to_join):
        ed = super(BERenderer, self).convert_to_printable_extract(extract_dict, feature_geometry, pdf_to_join)

        # Der Map-Parameter des Mapservers geht im PrintProxy verloren.
        # Er wird hier hardcoded eingefügt.
        # Der umständliche Weg via copy() und del wurde nötig, weil der
        # direkte Weg (einfaches Assign) aus irgendeinem mir nicht klaren
        # Grund nicht funktioniert hat.

        # Zunächst für die einzelnen ÖREB-Seiten
        for plr in ed['RealEstate_RestrictionOnLandownership']:
            for lyr in plr['baseLayers']['layers']:
                if 'https://oerebservice.apps.be.ch' in lyr['baseURL'] or 'https://oerebservice-test.apps.be.ch' in lyr['baseURL']:
                    if 'geodb.mopube_lif' in lyr['layers']:
                        customParams = lyr['customParams'].copy()
                        customParams['map'] = 'oerebav_de'
                        del lyr['customParams']
                        lyr['customParams'] = customParams
                    else:
                        customParams = lyr['customParams'].copy()
                        customParams['map'] = 'oereb_de'
                        del lyr['customParams']
                        lyr['customParams'] = customParams
            plr['baseLayers']['layers'].reverse()
        

        # Und hier noch für die Titelseite
        for lyr in ed['baseLayers']['layers']:
            if 'geodb.mopube_bbf' in lyr['layers']:
                customParams = lyr['customParams'].copy()
                customParams['map'] = 'oerebav_de'
                del lyr['customParams']
                lyr['customParams'] = customParams
            else:
                customParams = lyr['customParams'].copy()
                customParams['map'] = 'oereb_de'
                del lyr['customParams']
                lyr['customParams'] = customParams

        return ed

