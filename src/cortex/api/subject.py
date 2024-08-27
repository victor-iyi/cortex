"""## [Subjects]

A subject represents a human being who is the subject of a [record], ie
the person wearing the headset during the record. A subject is a
permanent object. It is stored on the hard drive and then synchronized
to the EMOTIV cloud.

To associate a subject to a record, you must create the subject first,
by calling [createSubject]. Then you must specify the subject name when
you call [createRecord]. A subject is identified by his/her name.

You can call [querySubjects] to list the subjects already created for
the current user.

[Subjects]:
https://emotiv.gitbook.io/cortex-api/subjects
 [record]: https://emotiv.gitbook.io/cortex-api/records [createSubject]:
https://emotiv.gitbook.io/cortex-api/subjects/createsubject
 [createRecord]:
https://emotiv.gitbook.io/cortex-api/records/createrecord
 [querySubjects]:
https://emotiv.gitbook.io/cortex-api/subjects/querysubjects

"""

# mypy: disable-error-code="assignment"

from collections.abc import Mapping
from typing import Literal, TypeAlias, TypedDict

from cortex.api.id import SubjectsID

# A dict with fields "from" and "to".
Interval = TypedDict('Interval', {'from': str, 'to': str})


class SubjectQuery(TypedDict, total=False):
    """Query parameters."""

    # Get a subject by its id.
    uuid: str

    # Filter the subjects by name.
    subjectName: str

    # Filter the subjects by their gender.
    sex: Literal['M', 'F', 'U']

    # Filter the subjects by their country code.
    countryCode: str

    # An object with fields "from" and "to" to filter
    # the subjects by their date of birth.
    dateOfBirth: Interval

    # An object with the fields as the keyword to
    # search and values are the list of fields to search.
    # The list of fields to search can contain
    # "subjectName", "lastName", "email".
    keyword: Mapping[str, str]


class Attribute(TypedDict):
    """Demographic attribute."""

    # The naem of the attribute.
    name: str

    # The value of the attribute.
    value: str


# Return Type Aliases.
CreateSubjectRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | list[Attribute]]]
UpdateSubjectRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str | list[Attribute]]]
DeleteSubjectRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str]]
QuerySubjectRequest: TypeAlias = Mapping[
    str, str | int | Mapping[str, str | SubjectQuery | int | list[Mapping[str, str]]]
]
DemoAttrRequest: TypeAlias = Mapping[str, str | int | Mapping[str, str]]


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
) -> CreateSubjectRequest:
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
        CreateSubjectRequest: The subject creation status.

    """
    _params = {
        'cortexToken': auth,
        'subjectName': subject_name,
    }

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

    _subject = {
        'id': SubjectsID.CREATE,
        'jsonrpc': '2.0',
        'method': 'createSubject',
        'params': _params,
    }

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
) -> UpdateSubjectRequest:
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
        UpdateSubjectRequest: The subject update status.

    """
    _params = {
        'cortexToken': auth,
        'subjectName': subject_name,
    }

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

    _subject = {
        'id': SubjectsID.UPDATE,
        'jsonrpc': '2.0',
        'method': 'updateSubject',
        'params': _params,
    }

    return _subject


def delete_subject(
    auth: str,
    subject_name: str,
) -> DeleteSubjectRequest:
    """Delete a subject.

    Args:
        auth (str): The Cortex authentication token.
        subject_name (str): The subject name.

    Read More:
        [deleteSubjects](https://emotiv.gitbook.io/cortex-api/subjects/deletesubjects)

    Returns:
        dict[str, str | int | dict[str, str]]: The subject deletion status.

    """
    _subject = {
        'id': SubjectsID.DELETE,
        'jsonrpc': '2.0',
        'method': 'deleteSubjects',
        'params': {
            'cortexToken': auth,
            'subjectName': subject_name,
        },
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
    _params = {
        'cortexToken': auth,
        'query': query,
        'orderBy': order_by,
    }

    if limit is not None:
        _params['limit'] = limit

    if offset is not None:
        _params['offset'] = offset

    _subject = {
        'id': SubjectsID.QUERY,
        'jsonrpc': '2.0',
        'method': 'querySubjects',
        'params': _params,
    }

    return _subject


def get_demographic_attr(auth: str) -> DemoAttrRequest:
    """Get the demographic attributes.

    Args:
        auth (str): The Cortex authentication token.

    Read More:
        [getDemographicAttributes](https://emotiv.gitbook.io/cortex-api/subjects/getdemographicattributes)

    Returns:
        DemoAttrRequest: The demographic attributes.

    """
    _subject = {
        'id': SubjectsID.DEMO_ATTR,
        'jsonrpc': '2.0',
        'method': 'getDemographicAttributes',
        'params': {
            'cortexToken': auth,
        },
    }

    return _subject
