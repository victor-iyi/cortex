"""## Subjects_.

A subject represents a human being who is the subject of a record_, ie the person wearing the headset during the
record. A subject is a permanent object. It is stored on the hard drive and then synchronized to the EMOTIV cloud.

To associate a subject to a record, you must create the subject first, by calling createSubject_. Then you must specify
the subject name when you call createRecord_. A subject is identified by his/her name.

You can call querySubjects_ to list the subjects already created for the current user.

.. _Subjects: https://emotiv.gitbook.io/cortex-api/subjects
.. _record: https://emotiv.gitbook.io/cortex-api/records
.. _createSubject: https://emotiv.gitbook.io/cortex-api/subjects/createsubject
.. _createRecord: https://emotiv.gitbook.io/cortex-api/records/createrecord
.. _querySubjects: https://emotiv.gitbook.io/cortex-api/subjects/querysubjects

"""

# mypy: disable-error-code="assignment"

from typing import Literal

from cortex.api.id import SubjectsID
from cortex.api.types import Attribute, BaseRequest, QuerySubjectRequest, SubjectQuery, SubjectRequest


def create_subject(
    auth: str,
    subject_name: str,
    *,
    date_of_birth: str | None = None,
    sex: Literal['M', 'F', 'U'] | None = None,
    country_code: str | None = None,
    state: str | None = None,
    city: str | None = None,
    attributes: list[Attribute] | None = None,
) -> SubjectRequest:
    """Create a subject.

    Args:
        auth (str): The Cortex authentication token.
        subject_name (str): The subject name.

    Keyword Args:
        date_of_birth (str, optional): The subject date of birth.
        sex (Literal['M', 'F', 'U'], optional): Subject's gender.
        country_code (str, optional): The subject country code.
        state (str, optional): The subject state.
        city (str, optional): The subject city.
        attributes (list[Attribute], optional): The subject attributes.

    Read More:
        [createSubject](https://emotiv.gitbook.io/cortex-api/subjects/createsubject)

    Returns:
        SubjectRequest: The subject creation status.

    """
    _params = {'cortexToken': auth, 'subjectName': subject_name}

    if date_of_birth is not None:
        _params['dateOfBirth'] = date_of_birth

    if sex is not None:
        _params['sex'] = sex

    if country_code is not None:
        _params['countryCode'] = country_code

    if state is not None:
        _params['state'] = state

    if city is not None:
        _params['city'] = city

    if attributes is not None:
        _params['attributes'] = attributes

    _subject = {'id': SubjectsID.CREATE, 'jsonrpc': '2.0', 'method': 'createSubject', 'params': _params}

    return _subject


def update_subject(
    auth: str,
    subject_name: str,
    *,
    date_of_birth: str | None = None,
    sex: Literal['M', 'F', 'U'] | None = None,
    country_code: str | None = None,
    state: str | None = None,
    city: str | None = None,
    attributes: list[Attribute] | None = None,
) -> SubjectRequest:
    """Update a subject.

    Args:
        auth (str): The Cortex authentication token.
        subject_name (str): The subject name.

    Keyword Args:
        date_of_birth (str, optional): The subject date of birth.
        sex (Literal['M', 'F', 'U'], optional): The gender of the subject.
        country_code (str, optional): The subject country code.
        state (str, optional): The subject state.
        city (str, optional): The subject city.
        attributes (list[Attribute], optional): The subject attributes.

    Read More:
        [updateSubject](https://emotiv.gitbook.io/cortex-api/subjects/querysubjects)

    Returns:
        SubjectRequest: The subject update status.

    """
    _params = {'cortexToken': auth, 'subjectName': subject_name}

    if date_of_birth is not None:
        _params['dateOfBirth'] = date_of_birth

    if sex is not None:
        _params['sex'] = sex

    if country_code is not None:
        _params['countryCode'] = country_code

    if state is not None:
        _params['state'] = state

    if city is not None:
        _params['city'] = city

    if attributes is not None:
        _params['attributes'] = attributes

    _subject = {'id': SubjectsID.UPDATE, 'jsonrpc': '2.0', 'method': 'updateSubject', 'params': _params}

    return _subject


def delete_subject(auth: str, subject_name: str) -> BaseRequest:
    """Delete a subject.

    Args:
        auth (str): The Cortex authentication token.
        subject_name (str): The subject name.

    Read More:
        [deleteSubjects](https://emotiv.gitbook.io/cortex-api/subjects/deletesubjects)

    Returns:
        BaseRequest: The subject deletion status.

    """
    _subject = {
        'id': SubjectsID.DELETE,
        'jsonrpc': '2.0',
        'method': 'deleteSubjects',
        'params': {'cortexToken': auth, 'subjectName': subject_name},
    }

    return _subject


def query_subject(
    auth: str,
    query: SubjectQuery,
    order_by: list[dict[str, Literal['ASC', 'DESC']]],
    *,
    limit: int | None = None,
    offset: int | None = None,
) -> QuerySubjectRequest:
    """Query a subject.

    Args:
        auth (str): The Cortex authentication token.
        query (Query): An object to filter the subjects.
        order_by (dict[str, Literal['ASC', 'DESC']]):
            Specify how to sort the subjects.

    Keyword Args:
        limit (int, optional): The maximum number of subjects to return.
        offset (int, optional): The number of subjects to skip.

    Read More:
        [querySubjects](https://emotiv.gitbook.io/cortex-api/subjects/querysubjects)

    Returns:
        QuerySubjectRequest: The subject query status.

    """
    _params = {'cortexToken': auth, 'query': query, 'orderBy': order_by}

    if limit is not None:
        _params['limit'] = limit

    if offset is not None:
        _params['offset'] = offset

    _subject = {'id': SubjectsID.QUERY, 'jsonrpc': '2.0', 'method': 'querySubjects', 'params': _params}

    return _subject


def get_demographic_attr(auth: str) -> BaseRequest:
    """Get the demographic attributes.

    Args:
        auth (str): The Cortex authentication token.

    Read More:
        [getDemographicAttributes](https://emotiv.gitbook.io/cortex-api/subjects/getdemographicattributes)

    Returns:
        BaseRequest: The demographic attributes.

    """
    _subject = {
        'id': SubjectsID.DEMO_ATTR,
        'jsonrpc': '2.0',
        'method': 'getDemographicAttributes',
        'params': {'cortexToken': auth},
    }

    return _subject
