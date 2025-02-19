import pytest

from utils.batch_processing import create_hubspot_batch_input, create_aws_batch_contacts
from hubspot.crm.contacts import BatchInputSimplePublicObjectBatchInputUpsert, SimplePublicObjectBatchInput

@pytest.fixture
def sample_contacts():
    return [
        {"email": "john.doe@example.com", "first_name": "John", "last_name": "Doe", "phone_number": "1234567890", "gender": "M"},
        {"email": "jane.smith@example.com", "first_name": "Jane", "last_name": "Smith", "phone_number": "0987654321", "gender": "F"}
    ]

def test_create_hubspot_batch_input(sample_contacts):

    expected_result = BatchInputSimplePublicObjectBatchInputUpsert(
        inputs=[
            SimplePublicObjectBatchInput(
                id_property="email",
                id="john.doe@example.com",
                properties={
                    "firstname": "John",
                    "lastname": "Doe",
                    "phone": "1234567890",
                    "gender": "M"
                }
            ),
            SimplePublicObjectBatchInput(
                id_property="email",
                id="jane.smith@example.com",
                properties={
                    "firstname": "Jane",
                    "lastname": "Smith",
                    "phone": "0987654321",
                    "gender": "F"
                }
            )
        ]
    )

    result = create_hubspot_batch_input(sample_contacts)

    assert result == expected_result

def test_create_aws_batch_contacts():

    contacts = [
        {"email": "john.doe@example.com"},
        {"email": "jane.smith@example.com"},
        {"email": "alex.jones@example.com"}
    ]

    expected_result = [
        [{"email": "john.doe@example.com"}, {"email": "jane.smith@example.com"}],
        [{"email": "alex.jones@example.com"}]
    ]
    BATCH_SIZE = 2
    result = create_aws_batch_contacts(contacts, BATCH_SIZE)

    assert result == expected_result
