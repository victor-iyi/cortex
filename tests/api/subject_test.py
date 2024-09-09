"""Test for subject module."""

import pytest

from collections.abc import Callable
from typing import Any, Final, TypeAlias

from cortex.api.subject import create_subject, update_subject, query_subject, delete_subject, get_demographic_attr
from cortex.api.id import SubjectsID
from cortex.api.types import Attribute, SubjectQuery

# Constants.
AUTH_TOKEN: Final[str] = '<AUTH-TOKEN>'

# Type aliases.
ResponseTemplate: TypeAlias = Callable[..., dict[str, Any]]


def test_create_subject(response_template: ResponseTemplate) -> None:
    """Test creating a subject."""
    subject_name = 'Subject name'
    date_of_birth = '1990-12-25'
    country_code = 'us'
    state = 'California'
    city = 'Los Angeles'
    attributes = [Attribute(name='age', value='20')]

    assert create_subject(AUTH_TOKEN, subject_name) == response_template(
        id=SubjectsID.CREATE, method='createSubject', params={'cortexToken': AUTH_TOKEN, 'subjectName': subject_name}
    )

    assert create_subject(
        AUTH_TOKEN, subject_name, date_of_birth=date_of_birth, country_code=country_code, attributes=attributes
    ) == response_template(
        id=SubjectsID.CREATE,
        method='createSubject',
        params={
            'cortexToken': AUTH_TOKEN,
            'subjectName': subject_name,
            'dateOfBirth': date_of_birth,
            'countryCode': country_code,
            'attributes': attributes,
        },
    )

    assert create_subject(
        AUTH_TOKEN,
        subject_name,
        date_of_birth=date_of_birth,
        sex='M',
        country_code=country_code,
        state=state,
        city=city,
        attributes=attributes,
    ) == response_template(
        id=SubjectsID.CREATE,
        method='createSubject',
        params={
            'cortexToken': AUTH_TOKEN,
            'subjectName': subject_name,
            'dateOfBirth': date_of_birth,
            'sex': 'M',
            'countryCode': country_code,
            'state': state,
            'city': city,
            'attributes': attributes,
        },
    )

    with pytest.raises(AssertionError, match='sex must be either "M", "F", or "U".'):
        create_subject(AUTH_TOKEN, subject_name, sex='invalid')


def test_update_subject(response_template: ResponseTemplate) -> None:
    """Test updating a subject."""
    subject_name = 'Subject name'
    date_of_birth = '1990-12-25'
    country_code = 'us'
    state = 'California'
    city = 'Los Angeles'
    attributes = [Attribute(name='age', value='20')]

    assert update_subject(AUTH_TOKEN, subject_name) == response_template(
        id=SubjectsID.UPDATE, method='updateSubject', params={'cortexToken': AUTH_TOKEN, 'subjectName': subject_name}
    )

    assert update_subject(
        AUTH_TOKEN,
        subject_name,
        date_of_birth=date_of_birth,
        sex='F',
        country_code=country_code,
        state=state,
        city=city,
        attributes=attributes,
    ) == response_template(
        id=SubjectsID.UPDATE,
        method='updateSubject',
        params={
            'cortexToken': AUTH_TOKEN,
            'subjectName': subject_name,
            'dateOfBirth': date_of_birth,
            'sex': 'F',
            'countryCode': country_code,
            'state': state,
            'city': city,
            'attributes': attributes,
        },
    )

    assert update_subject(AUTH_TOKEN, subject_name, date_of_birth=date_of_birth) == response_template(
        id=SubjectsID.UPDATE,
        method='updateSubject',
        params={'cortexToken': AUTH_TOKEN, 'subjectName': subject_name, 'dateOfBirth': date_of_birth},
    )


def test_delete_subject(response_template: ResponseTemplate) -> None:
    """Test deleting a subject."""
    subject_name = 'Subject name'

    assert delete_subject(AUTH_TOKEN, subject_name) == response_template(
        id=SubjectsID.DELETE, method='deleteSubjects', params={'cortexToken': AUTH_TOKEN, 'subjectName': subject_name}
    )


def test_query_subject(response_template: ResponseTemplate) -> None:
    """Test querying a subject."""
    query = SubjectQuery(
        date_of_birth={'from': '1990-12-25', 'to': '1995-12-25'},
        sex='F',
        country_code='us',
        keyword={'yyy': ['subjectName', 'email']},
    )
    order_by = [{'subjectName': 'ASC'}]

    assert query_subject(AUTH_TOKEN, query, order_by) == response_template(
        id=SubjectsID.QUERY,
        method='querySubjects',
        params={'cortexToken': AUTH_TOKEN, 'query': query, 'orderBy': order_by},
    )

    assert query_subject(AUTH_TOKEN, query, order_by, limit=1000) == response_template(
        id=SubjectsID.QUERY,
        method='querySubjects',
        params={'cortexToken': AUTH_TOKEN, 'query': query, 'orderBy': order_by, 'limit': 1000},
    )

    assert query_subject(AUTH_TOKEN, query, order_by, offset=3) == response_template(
        id=SubjectsID.QUERY,
        method='querySubjects',
        params={'cortexToken': AUTH_TOKEN, 'query': query, 'orderBy': order_by},
    )

    assert query_subject(AUTH_TOKEN, query, order_by, limit=1000, offset=10) == response_template(
        id=SubjectsID.QUERY,
        method='querySubjects',
        params={'cortexToken': AUTH_TOKEN, 'query': query, 'orderBy': order_by, 'limit': 1000, 'offset': 10},
    )

    with pytest.raises(ValueError, match='offset must be less than limit'):
        query_subject(AUTH_TOKEN, query, order_by, limit=2, offset=3)


def test_demographic_attr(response_template: ResponseTemplate) -> None:
    """Test getting demographic attributes."""
    assert get_demographic_attr(AUTH_TOKEN) == response_template(
        id=SubjectsID.DEMO_ATTR, method='getDemographicAttributes', params={'cortexToken': AUTH_TOKEN}
    )
