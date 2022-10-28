## Api Package

Every function / method has one test function. In this function are multiple tests.

### Async Functions

When testing an asynchronous the `@pytest.mark.asyncio` mark is used.

### Mocking / Patching

When something needs to be mocked or patched a MockerFixture is passed to the test function.

### disabling function

```python
mocker.patch('src.bluecurrent_api.websocket.Websocket._connect')
```

### changing return value

```python
     mocker.patch(
        'src.bluecurrent_api.websocket.Websocket._recv',
        return_value={"object": "STATUS_API_TOKEN",
                      "success": True, "token": "abc"}
    )
```

### Checking if function is called

```python
 test_send_request = mocker.patch("src.bluecurrent_api.client.Websocket.send_request")

 test_send_request.assert_called_with(
        {'command': 'START_SESSION', 'evse_id': '101', 'session_token': '123'})
```

### Checking if exception is raised

```python
with pytest.raises(WebsocketException):
        await websocket.get_charge_cards()
```

### Mocking an attribute or method of an object

```python
mocker.patch.object(Websocket, '_connection')


mock_send = mocker.patch.object(Websocket, '_send')
```

### AsyncMock

When a test needs to check if a async function is called an AsyncMock is used.

```python
test_close = mocker.patch(
        'src.bluecurrent_api.websocket.Websocket._connection.close',
        create=True,
        side_effect=AsyncMock()
    )
```

### test_send_to_receiver

In this test the receiver is mocked and then changed to an AsyncMock

```python
    mock_receiver = mocker.MagicMock()
    ...
    mock_receiver.assert_called_with('test')

    async_mock_receiver = AsyncMock()
    ...
    async_mock_receiver.assert_called_with('test')
```
