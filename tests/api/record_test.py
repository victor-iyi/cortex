"""Test for the record module."""

from collections.abc import Callable
from typing import Any, Final, TypeAlias

import pytest

from cortex.api.record import (
    create_record,
    stop_record,
    update_record,
    delete_record,
    export_record,
    query_records,
    record_infos,
    config_opt_out,
    download_record_data,
)
from cortex.api.id import RecordsID
from cortex.api.types import RecordQuery

# Constants.
AUTH_TOKEN: Final[str] = '<AUTH-TOKEN>'
SESSION_ID: Final[str] = '<SESSION-ID>'

# Type aliases.
ResponseTemplate: TypeAlias = Callable[..., dict[str, Any]]


def test_create_record(response_template: ResponseTemplate) -> None:
    """Test creating a record."""
    title = 'Record title'
    description = 'Record description'
    subject_name = 'Subject name'
    tags = ['tag1', 'tag2']
    experiment_id = 2

    assert create_record(AUTH_TOKEN, SESSION_ID, title) == response_template(
        id=RecordsID.CREATE,
        method='createRecord',
        params={'cortexToken': AUTH_TOKEN, 'session': SESSION_ID, 'title': title},
    )

    assert create_record(
        AUTH_TOKEN,
        SESSION_ID,
        title,
        description=description,
        subject_name=subject_name,
        tags=tags,
        experiment_id=experiment_id,
    ) == response_template(
        id=RecordsID.CREATE,
        method='createRecord',
        params={
            'cortexToken': AUTH_TOKEN,
            'session': SESSION_ID,
            'title': title,
            'description': description,
            'subjectName': subject_name,
            'tags': tags,
            'experimentId': experiment_id,
        },
    )


def test_stop_record(response_template: ResponseTemplate) -> None:
    """Test stopping a record."""
    assert stop_record(AUTH_TOKEN, SESSION_ID) == response_template(
        id=RecordsID.STOP, method='stopRecord', params={'cortexToken': AUTH_TOKEN, 'session': SESSION_ID}
    )


def test_update_record(response_template: ResponseTemplate) -> None:
    """Test updating a record."""
    record_id = 'd8fe7658-71f1-4cd6-bb5d-f6775b03438f'
    title = 'Record title'
    description = 'Record description'
    tags = ['tag1', 'tag2']

    assert update_record(AUTH_TOKEN, record_id) == response_template(
        id=RecordsID.UPDATE, method='updateRecord', params={'cortexToken': AUTH_TOKEN, 'record': record_id}
    )

    assert update_record(AUTH_TOKEN, record_id, title=title) == response_template(
        id=RecordsID.UPDATE,
        method='updateRecord',
        params={'cortexToken': AUTH_TOKEN, 'record': record_id, 'title': title},
    )

    assert update_record(AUTH_TOKEN, record_id, title=title, description=description, tags=tags) == response_template(
        id=RecordsID.UPDATE,
        method='updateRecord',
        params={
            'cortexToken': AUTH_TOKEN,
            'record': record_id,
            'title': title,
            'description': description,
            'tags': tags,
        },
    )


def test_delete_record(response_template: ResponseTemplate) -> None:
    """Test deleting a record."""
    records = ['d8fe7658-71f1-4cd6-bb5d-f6775b03438f', 'invalid-id']

    assert delete_record(AUTH_TOKEN, records) == response_template(
        id=RecordsID.DELETE, method='deleteRecord', params={'cortexToken': AUTH_TOKEN, 'records': records}
    )


def test_export_record(response_template: ResponseTemplate) -> None:
    """Test exporting a record."""
    records = ['d8fe7658-71f1-4cd6-bb5d-f6775b03438f', 'ec0ac33f-ad4e-48b1-bbc3-8502f5c49b62']
    folder = '/tmp/cortex'
    stream_types = ['EEG', 'MOTION']
    license_ids = ['license1']

    assert export_record(AUTH_TOKEN, records, folder, stream_types, 'CSV') == response_template(
        id=RecordsID.EXPORT,
        method='exportRecord',
        params={
            'cortexToken': AUTH_TOKEN,
            'recordIds': records,
            'folder': folder,
            'streamTypes': stream_types,
            'format': 'CSV',
        },
    )

    assert export_record(AUTH_TOKEN, records, folder, stream_types, 'CSV', version='V1') == response_template(
        id=RecordsID.EXPORT,
        method='exportRecord',
        params={
            'cortexToken': AUTH_TOKEN,
            'recordIds': records,
            'folder': folder,
            'streamTypes': stream_types,
            'format': 'CSV',
            'version': 'V1',
        },
    )

    assert export_record(AUTH_TOKEN, records, folder, stream_types, 'EDFPLUS', version='V1') == response_template(
        id=RecordsID.EXPORT,
        method='exportRecord',
        params={
            'cortexToken': AUTH_TOKEN,
            'recordIds': records,
            'folder': folder,
            'streamTypes': stream_types,
            'format': 'EDFPLUS',
        },
    )

    with pytest.raises(AssertionError, match='format must be either "EDF", "EDFPLUS", "BDFPLUS", or "CSV".'):
        export_record(AUTH_TOKEN, records, folder, stream_types, 'invalid')

    assert export_record(
        AUTH_TOKEN,
        records,
        folder,
        stream_types,
        'CSV',
        version='V1',
        license_ids=license_ids,
        include_survey=True,
        include_demographics=True,
        include_deprecated_pm=True,
        include_marker_extra_infos=True,
    ) == response_template(
        id=RecordsID.EXPORT,
        method='exportRecord',
        params={
            'cortexToken': AUTH_TOKEN,
            'recordIds': records,
            'folder': folder,
            'streamTypes': stream_types,
            'format': 'CSV',
            'version': 'V1',
            'licenseIds': license_ids,
            'includeDemographics': True,
            'includeSurvey': True,
            'includeMarkerExtraInfos': True,
            'includeDeprecatedPM': True,
        },
    )


def test_query_records(response_template: ResponseTemplate) -> None:
    """Test querying records."""
    query = RecordQuery(
        licenseId='license1',
        applicationId='com.cortex.example',
        keyword='Cortex Example',
        startDatetime={'from': 0, 'to': 1},
        modifiedDatetime={'from': 0, 'to': 1},
        duration={'from': 0, 'to': 1},
    )
    order_by = [{'startDatetime': 'DESC'}, {'title': 'ASC'}]

    assert query_records(AUTH_TOKEN, query, order_by) == response_template(
        id=RecordsID.QUERY,
        method='queryRecords',
        params={'cortexToken': AUTH_TOKEN, 'query': query, 'orderBy': order_by},
    )

    assert query_records(AUTH_TOKEN, query, order_by, offset=2) == response_template(
        id=RecordsID.QUERY,
        method='queryRecords',
        params={'cortexToken': AUTH_TOKEN, 'query': query, 'orderBy': order_by},
    )

    assert query_records(AUTH_TOKEN, RecordQuery(licenseId='license1'), order_by) == response_template(
        id=RecordsID.QUERY,
        method='queryRecords',
        params={'cortexToken': AUTH_TOKEN, 'query': {'licenseId': 'license1'}, 'orderBy': order_by},
    )

    assert query_records(
        AUTH_TOKEN, query, order_by, limit=100, offset=2, include_markers=True, include_sync_status_info=True
    ) == response_template(
        id=RecordsID.QUERY,
        method='queryRecords',
        params={
            'cortexToken': AUTH_TOKEN,
            'query': query,
            'orderBy': order_by,
            'limit': 100,
            'offset': 2,
            'includeMarkers': True,
            'includeSyncStatusInfo': True,
        },
    )


def test_record_infos(response_template: ResponseTemplate) -> None:
    """Test getting record information."""
    records = ['d8fe7658-71f1-4cd6-bb5d-f6775b03438f', 'ec0ac33f-ad4e-48b1-bbc3-8502f5c49b62']

    assert record_infos(AUTH_TOKEN, records) == response_template(
        id=RecordsID.INFO, method='getRecordInfos', params={'cortexToken': AUTH_TOKEN, 'recordIds': records}
    )


def test_config_opt_out(response_template: ResponseTemplate) -> None:
    """Test configuring opt-out."""
    assert config_opt_out(AUTH_TOKEN, 'get') == response_template(
        id=RecordsID.CONFIG_OPT_OUT, method='configOptOut', params={'cortexToken': AUTH_TOKEN, 'status': 'get'}
    )

    assert config_opt_out(AUTH_TOKEN, 'set', new_opt_out=True) == response_template(
        id=RecordsID.CONFIG_OPT_OUT,
        method='configOptOut',
        params={'cortexToken': AUTH_TOKEN, 'status': 'set', 'newOptOut': True},
    )

    assert config_opt_out(AUTH_TOKEN, 'set') == response_template(
        id=RecordsID.CONFIG_OPT_OUT,
        method='configOptOut',
        params={'cortexToken': AUTH_TOKEN, 'status': 'set', 'newOptOut': False},
    )

    with pytest.raises(AssertionError, match='status must be either "get" or "set".'):
        config_opt_out(AUTH_TOKEN, 'invalid')


def test_download_record(response_template: ResponseTemplate) -> None:
    """Test downloading a record."""
    records = ['d8fe7658-71f1-4cd6-bb5d-f6775b03438f', 'ec0ac33f-ad4e-48b1-bbc3-8502f5c49b62']

    assert download_record_data(AUTH_TOKEN, records) == response_template(
        id=RecordsID.DOWNLOAD_DATA,
        method='requestToDownloadRecordData',
        params={'cortexToken': AUTH_TOKEN, 'recordIds': records},
    )
