from hubspot.crm.contacts import BatchInputSimplePublicObjectBatchInputUpsert, SimplePublicObjectBatchInput
from config.settings import HUBSPOT_UPSERT_CONTACT_BATCH_SIZE

def create_hubspot_batch_input(contacts):
    return BatchInputSimplePublicObjectBatchInputUpsert(
        inputs=[
            SimplePublicObjectBatchInput(
                id_property="email",
                id=contact["email"],
                properties={
                    "firstname": contact["first_name"],
                    "lastname": contact["last_name"],
                    "phone": contact["phone_number"],
                    "gender": contact["gender"]
                }
            ) for contact in contacts if contact.get("email")
        ]
    )

def create_aws_batch_contacts(contacts, batch_size = HUBSPOT_UPSERT_CONTACT_BATCH_SIZE):
    return [
        contacts[i : i + batch_size]
        for i in range(0, len(contacts), batch_size)
    ]
