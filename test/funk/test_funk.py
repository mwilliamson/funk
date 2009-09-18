import funk

@funk.with_context
def test_can_create_a_fake_object(context):
    fake = context.fake()
