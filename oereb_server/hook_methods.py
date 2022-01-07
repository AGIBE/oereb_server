# -*- coding: utf-8 -*-
import datetime
from pyramid.path import DottedNameResolver
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy import cast, Text
from pyramid_oereb import Config, database_adapter
from pyramid_oereb.core.records.office import OfficeRecord
from pyramid_oereb.contrib.data_sources.standard.sources.plr import StandardThemeConfigParser

def get_surveying_data_provider(real_estate):
    """
    Args:
        real_estate (pyramid_oereb.lib.records.real_estate.RealEstateRecord): The real estate for which the
            provider of the surveying data should be delivered.
    Returns:
        provider (pyramid_oereb.lib.records.office.OfficeRecord): The provider who produced the used
            surveying data.
    """
    params = Config.get_real_estate_config().get('source').get('params')
    session = database_adapter.get_session(params.get('db_connection'))
    try:
        model = DottedNameResolver().resolve(params.get('model'))
        re = session.query(model).filter(model.egrid == real_estate.egrid).one()
        provider = OfficeRecord(re.data_provider)
        return provider
    finally:
        session.close()


def get_surveying_data_update_date(real_estate):
    """
    Gets the date of the latest update of the used survey data data for the
    situation map. The method you find here is only matching the standard configuration. But you can provide
    your own one if your configuration is different. The only thing you need to take into account is that the
    input of this method is always and only a real estate record. And the output of this method must be a
    datetime.date object.
    Args:
        real_estate (pyramid_oereb.lib.records.real_estate.RealEstateRecord): The real
            estate for which the last update date of the base data should be indicated
    Returns:
        update_date (datetime.datetime): The date of the last update of the cadastral base data
    """
    params = Config.get_real_estate_config().get('source').get('params')
    session = database_adapter.get_session(params.get('db_connection'))
    try:
        model = DottedNameResolver().resolve(params.get('model'))
        re = session.query(model).filter(model.egrid == real_estate.egrid).one()
        return datetime.datetime.combine(re.currentness, datetime.time.min)
    finally:
        session.close()

def get_symbol_ref(request, record):
    """
    Returns the link to the symbol of the specified public law restriction.
    The link is taken form the field symbol_url.
    Function is based on pyramid_oereb.contrib.data_sources.standard.hook_methods.get_symbol

    Args:
        request (pyramid.request.Request): The current request instance.
        record (pyramid_oereb.core.records.plr.PlrRecord or
            pyramid_oereb.core.records.view_service.LegendEntryRecord): The record of the public law
            restriction to get the symbol reference for.

    Returns:
        uri: The link to the symbol for the specified public law restriction.
    """
    plr = None
    for p in Config.get('plrs'):
        if str(p.get('code')).lower() == str(record.theme.code).lower():
            plr = p
            break

    if plr is None:
        raise HTTPNotFound('No theme with code {}.'.format(record.theme.code))

    params = plr['source']['params']
    session = database_adapter.get_session(params.get('db_connection'))
    try:
        config_parser = StandardThemeConfigParser(**plr)
        models = config_parser.get_models()
        model = models.LegendEntry
        legend_entry = session.query(model).filter(
            cast(model.type_code, Text) == cast(record.type_code, Text)
        ).filter(
            cast(model.type_code_list, Text) == cast(record.type_code_list, Text)
        ).filter(
            model.view_service_id == record.view_service_id
        ).first()
        if legend_entry:
            symbol_url = getattr(legend_entry, 'symbol_url', None)
            if symbol_url:
                return symbol_url
        raise HTTPNotFound()
    finally:
        session.close()
        