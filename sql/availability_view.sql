-- Dieser View liegt im Schema oereb_server und zieht alle
-- Infos bezüglich Verfügbarkeit der Themen zusammen.
-- Er vereinigt alle availability-Tabellen aller aufgeschalteten
-- Themen. Bei neu aufzuschaltenden Themen muss er auch aktualisiert werden.

CREATE OR REPLACE VIEW oereb_server.availability
AS SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BaulinienFlughafenanlagen'::text AS theme_code,
    availability.available
   FROM airports_building_lines2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.ProjektierungszonenFlughafenanlagen'::text AS theme_code,
    availability.available
   FROM airports_project_planning_zones2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.Sicherheitszonenplan'::text AS theme_code,
    availability.available
   FROM airports_security_zone_plans2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BE.ArchaeologischesInventar'::text AS theme_code,
    availability.available
   FROM archaeological_inventory2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BE.KantonaleWaldabstandslinien'::text AS theme_code,
    availability.available
   FROM cantonal_forest_distance_lines2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BE.KantonaleNutzungsplanung'::text AS theme_code,
    availability.available
   FROM cantonal_land_use_plans2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BE.KantonaleNaturschutzgebiete'::text AS theme_code,
    availability.available
   FROM cantonal_nature_reserves2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BE.KantonaleLaermempfindlichkeitsstufen'::text AS theme_code,
    availability.available
   FROM cantonal_noise_sensitivity_levels2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BE.KantonalePlanungszonen'::text AS theme_code,
    availability.available
   FROM cantonal_planning_zones2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BE.BaulinienKantonsstrassen'::text AS theme_code,
    availability.available
   FROM cantonal_street_building_lines2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BE.KantonalerGewaesserraum'::text AS theme_code,
    availability.available
   FROM cantonal_water_space2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BelasteteStandorteZivileFlugplaetze'::text AS theme_code,
    availability.available
   FROM contaminated_civil_aviation_sites2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BelasteteStandorteMilitaer'::text AS theme_code,
    availability.available
   FROM contaminated_military_sites2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BelasteteStandorteOeffentlicherVerkehr'::text AS theme_code,
    availability.available
   FROM contaminated_public_transport_sites2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BelasteteStandorte'::text AS theme_code,
    availability.available
   FROM contaminated_sites2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BE.Ueberflutungsgebiet'::text AS theme_code,
    availability.available
   FROM flood_areas2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.Waldabstandslinien'::text AS theme_code,
    availability.available
   FROM forest_distance_lines2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.StatischeWaldgrenzen'::text AS theme_code,
    availability.available
   FROM forest_perimeters2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.Waldreservate'::text AS theme_code,
    availability.available
   FROM forest_reserves2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.Grundwasserschutzareale'::text AS theme_code,
    availability.available
   FROM groundwater_protection_sites2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.Grundwasserschutzzonen'::text AS theme_code,
    availability.available
   FROM groundwater_protection_zones2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BaulinienStarkstromanlagen'::text AS theme_code,
    availability.available
   FROM heavy_current_installations_building_lines2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.ProjektierungszonenStarkstromanlagen'::text AS theme_code,
    availability.available
   FROM heavy_current_installations_planning_zones2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.Nutzungsplanung'::text AS theme_code,
    availability.available
   FROM land_use_plans2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BaulinienNationalstrassen'::text AS theme_code,
    availability.available
   FROM motorways_building_lines2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.ProjektierungszonenNationalstrassen'::text AS theme_code,
    availability.available
   FROM motorways_project_planing_zones2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.Laermempfindlichkeitsstufen'::text AS theme_code,
    availability.available
   FROM noise_sensitivity_levels2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.Planungszonen'::text AS theme_code,
    availability.available
   FROM planning_zones2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BaulinienEisenbahnanlagen'::text AS theme_code,
    availability.available
   FROM railways_building_lines2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.ProjektierungszonenEisenbahnanlagen'::text AS theme_code,
    availability.available
   FROM railways_project_planning_zones2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BE.RegionaleWaldabstandslinien'::text AS theme_code,
    availability.available
   FROM regional_forest_distance_lines2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BE.RegionaleNutzungsplanung'::text AS theme_code,
    availability.available
   FROM regional_land_use_plans2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BE.RegionaleLaermempfindlichkeitsstufen'::text AS theme_code,
    availability.available
   FROM regional_noise_sensitivity_levels2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BE.RegionalePlanungszonen'::text AS theme_code,
    availability.available
   FROM regional_planning_zones2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BE.GeschuetzteBotanischeObjekte'::text AS theme_code,
    availability.available
   FROM regional_protected_botanical_objects2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BE.GeschuetzteGeologischeObjekte'::text AS theme_code,
    availability.available
   FROM regional_protected_geological_objects2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BE.RegionalerGewaesserraum'::text AS theme_code,
    availability.available
   FROM regional_water_space2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.Gewaesserraum'::text AS theme_code,
    availability.available
   FROM water_space2.availability
UNION
 SELECT gen_random_uuid() AS id,
    availability.fosnr AS municipality_fosnr,
    'ch.BE.LeitungenWasser'::text AS theme_code,
    availability.available
   FROM conduits_water2.availability
UNION
 SELECT gen_random_uuid() as id,
 availability.fosnr AS municipality_fosnr,
 'ch.BE.Gewaesserschutzbereiche'::text AS theme_code,
 availability.available
 FROM water_protection_areas2.availability;

-- Permissions

ALTER TABLE oereb_server.availability OWNER TO oereb;
GRANT ALL ON TABLE oereb_server.availability TO oereb;
GRANT SELECT ON TABLE oereb_server.availability TO oereb_viewer;
