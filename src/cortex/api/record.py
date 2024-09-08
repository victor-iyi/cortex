"""## Records_.

After you opened a session_ with a headset, you can create a record. A record is a permanent object to store data from
an EMOTIV headset. You can associate a subject_ to a record. You can add one or more markers_ to a record.

Unlike a session_, a record is a permanent object. It is stored on the hard drive and then can be synchronized to the
EMOTIV cloud. The `opt-out`_ configuration can let you decide if the records of a user are uploaded to the cloud or not.

.. _Records: https://emotiv.gitbook.io/cortex-api/records
.. _session: https://emotiv.gitbook.io/cortex-api/session
.. _subject: https://emotiv.gitbook.io/cortex-api/subjects
.. _markers: https://emotiv.gitbook.io/cortex-api/markers
.. _`opt-out`: https://emotiv.gitbook.io/cortex-api/records/configoptout

"""

# mypy: disable-error-code="assignment"

from typing import Literal

from cortex.api.id import RecordsID
from cortex.api.types import (
    BaseRequest,
    ConfigOptOutRequest,
    CreateRecordRequest,
    DeleteRecordRequest,
    DownloadRecordDataRequest,
    ExportRecordRequest,
    QueryRecordRequest,
    RecordInfoRequest,
    RecordQuery,
    UpdateRecordRequest,
)


def create_record(
    auth: str,
    session_id: str,
    title: str,
    *,
    description: str | None = None,
    subject_name: str | None = None,
    tags: list[str] | None = None,
    experiment_id: int | None = None,
) -> CreateRecordRequest:
    """Create a record.

    Args:
        auth (str): The Cortex authentication token.
        session_id (str): The session ID.
        title (str): The record title.

    Keyword Args:
        description (str, optional): The record description.
        subject_name (str, optional): The subject name.
        tags (list[str], optional): The record tags.
        experiment_id (int, optional): The experiment ID.

    Read More:
        ['createRecord](https://emotiv.gitbook.io/cortex-api/records/createrecord)

    Returns:
        CreateRecordRequest: The record creation status.

    """
    _params = {'cortexToken': auth, 'session': session_id, 'title': title}

    if description is not None:
        _params['description'] = description

    if subject_name is not None:
        _params['subjectName'] = subject_name

    if tags is not None:
        _params['tags'] = tags

    if experiment_id is not None:
        _params['experimentId'] = experiment_id

    _record = {'id': RecordsID.CREATE, 'jsonrpc': '2.0', 'method': 'createRecord', 'params': _params}

    return _record


def stop_record(auth: str, session_id: str) -> BaseRequest:
    """Stop the record.

    Args:
        auth (str): The Cortex authentication token.
        session_id (str): The session ID.

    Read More:
        [stopRecord](https://emotiv.gitbook.io/cortex-api/records/stoprecord)

    Returns:
        BaseRequest: The record stop status.

    """
    _record = {
        'id': RecordsID.STOP,
        'jsonrpc': '2.0',
        'method': 'stopRecord',
        'params': {'cortexToken': auth, 'session': session_id},
    }

    return _record


def update_record(
    auth: str,
    record_id: str,
    *,
    title: str | None = None,
    description: str | None = None,
    tags: list[str] | None = None,
) -> UpdateRecordRequest:
    """Update the record.

    Args:
        auth (str): The Cortex authentication token.
        record_id (str): The record ID.

    Keyword Args:
        title (str, optional): The record title.
        description (str, optional): The record description.
        tags (list[str], optional): The new tags of the record.

    Read More:
        [updateRecord](https://emotiv.gitbook.io/cortex-api/records/updaterecord)

    Returns:
        UpdateRecordRequest: The record update status.

    """
    _params = {'cortexToken': auth, 'record': record_id}

    if title is not None:
        _params['title'] = title

    if description is not None:
        _params['description'] = description

    if tags is not None:
        _params['tags'] = tags

    _record = {'id': RecordsID.UPDATE, 'jsonrpc': '2.0', 'method': 'updateRecord', 'params': _params}

    return _record


def delete_record(auth: str, records: list[str]) -> DeleteRecordRequest:
    """Delete a record.

    Args:
        auth (str): The Cortex authentication token.
        records (list[str]): The record IDs.

    Read More:
        [deleteRecord](https://emotiv.gitbook.io/cortex-api/records/deleterecord)

    Returns:
        DeleteRecordRequest: The record deletion status.

    """
    _record = {
        'id': RecordsID.DELETE,
        'jsonrpc': '2.0',
        'method': 'deleteRecord',
        'params': {'cortexToken': auth, 'records': records},
    }

    return _record


def export_record(
    auth: str,
    record_ids: list[str],
    folder: str,
    stream_types: list[str],
    # pylint: disable-next=redefined-builtin
    format: Literal['EDF', 'EDFPLUS', 'BDFPLUS', 'CSV'],
    *,
    version: Literal['V1', 'V2'] | None = None,
    license_ids: list[str] | None = None,
    include_demographics: bool = False,
    include_survey: bool = False,
    include_marker_extra_infos: bool = False,
    include_deprecated_pm: bool = False,
) -> ExportRecordRequest:
    """Export one or more records to EDF or CSV files.

    Args:
        auth (str): The Cortex authentication token.
        record_ids (list[str]): The record IDs.
        folder (str): The path of a local folder.
        stream_types (list[str]): List of the data streams you want to export.
        format (Literal['EDF' 'EDFPLUS', 'BDFPLUS', 'CSV']): The format of the
             exported files.

    Keyword Args:
        version (Literal['V1', 'V2']): The version of the CSV format.
             If the format is "EDF", then you must omit this parameter.
             If the format is "CSV", then this parameter must be "V1" or "V2".
        license_ids (list[str], optional): The default value is an empty list,
             which means that you can only export the records created by your app.
        include_demographics (bool, optional): If `true` the the exported JSON
             file will include the demographic data of the user.
        include_survey (bool, optional): If `true` the the exported JSON file
             will include the survey data of the record.
        include_marker_extra_infos (bool, optional): If `true` the the markers of
             the records will be exported to a CSV file.
        include_deprecated_pm (bool, optional): If `true` then deprecated performance
             metrics (i.e. Focus) will be exported.

    Read More:
        [exportRecord](https://emotiv.gitbook.io/cortex-api/records/exportrecord)

    Returns:
        ExportRecordRequest: The record export status.

    """
    assert format in [
        'EDF',
        'EDFPLUS',
        'BDFPLUS',
        'CSV',
    ], 'format must be either "EDF", "EDFPLUS", "BDFPLUS", or "CSV".'

    _params = {
        'cortexToken': auth,
        'recordIds': record_ids,
        'folder': folder,
        'streamTypes': stream_types,
        'format': format,
    }

    if format == 'CSV' and version is not None:
        _params['version'] = version

    if license_ids is not None:
        _params['licenseIds'] = license_ids

    if include_demographics:
        _params['includeDemographics'] = include_demographics

    if include_survey:
        _params['includeSurvey'] = include_survey

    if include_marker_extra_infos:
        _params['includeMarkerExtraInfos'] = include_marker_extra_infos

    if include_deprecated_pm:
        _params['includeDeprecatedPM'] = include_deprecated_pm

    _record = {'id': RecordsID.EXPORT, 'jsonrpc': '2.0', 'method': 'exportRecord', 'params': _params}

    return _record


def query_records(
    auth: str,
    query: RecordQuery,
    order_by: list[dict[str, Literal['ASC', 'DESC']]],
    *,
    limit: int | None = None,
    offset: int | None = None,
    include_markers: bool = False,
    include_sync_status_info: bool = False,
) -> QueryRecordRequest:
    """Query the records.

    Args:
        auth (str): The Cortex authentication token.
        query (Query): An object to filter the records.
        order_by (dict[str, Literal['ASC', 'DESC']]):
            Specify how to sort the records.

    Keyword Args:
        limit (int, optional): The maximum number of records to return.
        offset (int, optional): The number of records to skip.
        include_markers (bool, optional): If `true` then the markers of the records
            will be included in the response.
        include_sync_status_info (bool, optional): If `true` then the synchronization
            status of the records will be included in the response.

    Read More:
        [queryRecords](https://emotiv.gitbook.io/cortex-api/records/queryrecords)

    Returns:
        QuerySubjectRequest: The record query status.

    """
    _params = {'cortexToken': auth, 'query': query, 'orderBy': order_by}

    if limit is not None:
        _params['limit'] = limit

    if offset is not None and limit is not None:
        _params['offset'] = offset

    if include_markers:
        _params['includeMarkers'] = include_markers

    if include_sync_status_info:
        _params['includeSyncStatusInfo'] = include_sync_status_info

    _record = {'id': RecordsID.QUERY, 'jsonrpc': '2.0', 'method': 'queryRecords', 'params': _params}

    return _record


def record_infos(auth: str, record_ids: list[str]) -> RecordInfoRequest:
    """Get the record information.

    Args:
        auth (str): The Cortex authentication token.
        record_ids (list[str]): The record IDs.

    Read More:
        [getRecordInformation](https://emotiv.gitbook.io/cortex-api/records/getrecordinfos)

    Returns:
        RecordInfoRequest: The record information.

    """
    _record = {
        'id': RecordsID.INFO,
        'jsonrpc': '2.0',
        'method': 'getRecordInfos',
        'params': {'cortexToken': auth, 'recordIds': record_ids},
    }

    return _record


def config_opt_out(auth: str, status: Literal['get', 'set'], *, new_opt_out: bool = False) -> ConfigOptOutRequest:
    """Get or set the opt-out status.

    Args:
        auth (str): The Cortex authentication token.
        status (Literal['get', 'set']): The opt-out status.

    Keyword Args:
        new_opt_out (bool, optional): The new opt-out status.

    Read More:
        [configOptOut](https://emotiv.gitbook.io/cortex-api/records/configoptout)

    Returns:
        ConfigOptOutRequest: The opt-out status.

    """
    assert status in ['get', 'set'], 'status must be either "get" or "set".'

    _params = {'cortexToken': auth, 'status': status}
    if status == 'set':
        _params['newOptOut'] = new_opt_out

    _record = {'id': RecordsID.CONFIG_OPT_OUT, 'jsonrpc': '2.0', 'method': 'configOptOut', 'params': _params}

    return _record


def download_record_data(auth: str, record_ids: list[str]) -> DownloadRecordDataRequest:
    """Download record data.

    Args:
        auth (str): The Cortex authentication token.
        record_ids (list[str]): The record IDs.

    Read More:
        [requestToDownloadRecordData](https://emotiv.gitbook.io/cortex-api/records/requesttodownloadrecorddata)

    Returns:
        DownloadRecordDataRequest: The record data.

    """
    _record = {
        'id': RecordsID.DOWNLOAD_DATA,
        'jsonrpc': '2.0',
        'method': 'requestToDownloadRecordData',
        'params': {'cortexToken': auth, 'recordIds': record_ids},
    }

    return _record
