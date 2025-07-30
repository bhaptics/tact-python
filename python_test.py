import bhaptics_python
import asyncio
import time

async def main():
    print("Hello World")
    app_id = ""
    api_key = ""
    app_version = -1
    result = await bhaptics_python.registry_and_initialize(app_id,api_key,"")
    print(result)
    device_index = 1
    while True:
        user_input = input("input ('q': exit): ").strip()
        request_id = 0
        device_address = ""
        device_address_swap = ""
        event_name = ""

        if user_input == 'q':
            print("program exit")
            break
        elif user_input == '':
            continue
        elif user_input == 'p':
            request_id = await bhaptics_python.play_event(event_name)
            print(f"{event_name} play_event request_id : {request_id}")
        elif user_input == 'pd':
            request_id = await bhaptics_python.play_event(event_name, device_index)
            print(f"{event_name} play_event request_id : {request_id}")
        elif user_input == 's':
            await bhaptics_python.stop_by_request_id(request_id)
        elif user_input == 'o':
            await bhaptics_python.stop_by_event_name(event_name)
        elif user_input == 'a':
            await bhaptics_python.stop_all()
        elif user_input == 'd':
            motor_len = 40
            values = [0 for _ in range(motor_len)]

            for i in range(motor_len):
                values[i] = 40
                if i > 0:
                    values[i - 1] = 0

                request_id = await bhaptics_python.play_dot(0, 1000, values)
                time.sleep(1)
        elif user_input == 'dd':
            motor_len = 40
            values = [0 for _ in range(motor_len)]

            for i in range(motor_len):
                values[i] = 40
                if i > 0:
                    values[i - 1] = 0

                request_id = await bhaptics_python.play_dot(0, 1000, values, device_index)
                time.sleep(1)
        elif user_input == 'path':
            x = [0.738, 0.723, 0.709, 0.696, 0.682, 0.667, 0.653, 0.639, 0.624, 0.611, 0.597, 0.584, 0.57, 0.557, 0.542, 0.528, 0.515, 0.501, 0.487, 0.474, 0.46, 0.447, 0.432, 0.419, 0.406, 0.393, 0.378, 0.365, 0.352, 0.338, 0.324, 0.311, 0.297]
            y = [0.68, 0.715, 0.749, 0.782, 0.816, 0.852, 0.885, 0.921, 0.956, 0.952, 0.918, 0.885, 0.848, 0.816, 0.779, 0.743, 0.71, 0.673, 0.639, 0.606, 0.571, 0.537, 0.5, 0.467, 0.434, 0.4, 0.363, 0.329, 0.296, 0.261, 0.226, 0.192, 0.157]
            values = [40 for _ in range(len(x))]

            for i in range(len(x)):
                slice_x = [x[i]]
                slice_y = [y[i]]
                slice_intensity = [values[i]]

                request_id = await bhaptics_python.play_path(0, 1000, slice_x, slice_y, slice_intensity)
                time.sleep(1)
        elif user_input == 'pathd':
            x = [0.738, 0.723, 0.709, 0.696, 0.682, 0.667, 0.653, 0.639, 0.624, 0.611, 0.597, 0.584, 0.57, 0.557, 0.542, 0.528, 0.515, 0.501, 0.487, 0.474, 0.46, 0.447, 0.432, 0.419, 0.406, 0.393, 0.378, 0.365, 0.352, 0.338, 0.324, 0.311, 0.297]
            y = [0.68, 0.715, 0.749, 0.782, 0.816, 0.852, 0.885, 0.921, 0.956, 0.952, 0.918, 0.885, 0.848, 0.816, 0.779, 0.743, 0.71, 0.673, 0.639, 0.606, 0.571, 0.537, 0.5, 0.467, 0.434, 0.4, 0.363, 0.329, 0.296, 0.261, 0.226, 0.192, 0.157]
            values = [40 for _ in range(len(x))]

            for i in range(len(x)):
                slice_x = [x[i]]
                slice_y = [y[i]]
                slice_intensity = [values[i]]

                request_id = await bhaptics_python.play_path(0, 1000, slice_x, slice_y, slice_intensity, device_index)
                time.sleep(1)
        elif user_input == 'g':
            glove_len  = 8
            repeat_count = 0
            motors = [100 for _ in range(glove_len)]
            playtimes = [8 for _ in range(glove_len)]
            shapes = [2 for _ in range(glove_len)]

            for _ in range(5):
                await bhaptics_python.play_glove(8, motors, playtimes, shapes, repeat_count)
                time.sleep(0.04)

            time.sleep(0.5)

            for _ in range(5):
                await bhaptics_python.play_glove(9, motors, playtimes, shapes, repeat_count)
                time.sleep(0.04)
        elif user_input == 'ping':
            await bhaptics_python.ping(device_address)
        elif user_input == 'pinga':
            await bhaptics_python.ping_all()
        elif user_input == 'vsm':
            await bhaptics_python.set_device_vsm(device_address, 400)
        elif user_input == 'swap':
            await bhaptics_python.swap_position(device_address_swap)
        elif user_input == 'event':
            event_time = await bhaptics_python.get_event_time(event_name)
            print(f"get_event_time({event_name}) : {event_time}")
        elif user_input == 'i':
            print(f"{event_name} is_playing_event_by_request_id ({request_id}) {await bhaptics_python.is_playing_event_by_request_id(request_id)}")
            print(f"{event_name} is_playing_event_by_event_id {await bhaptics_python.is_playing_event_by_event_id(event_name)}")
            print(f"is_playing_event {await bhaptics_python.is_playing_event()}")
        elif user_input == 'json':
            print(f"get_device_info_json {await bhaptics_python.get_device_info_json()}")
            print(f"get_haptic_mappings_json {await bhaptics_python.get_haptic_mappings_json()}")
        elif user_input == 'haptic':
            message = await bhaptics_python.get_haptic_messages(app_id, api_key, app_version)
            mappings = await bhaptics_python.get_haptic_mappings(app_id, api_key, app_version)

            print(f"get_haptic_messages {message}")
            print(f"get_haptic_mappings {mappings}")
        elif user_input == 'position':
            for i in range(10):
                print(f"is_bhaptics_connected({i}) {await bhaptics_python.is_bhaptics_device_connected(i)}")
        elif user_input == 'loop':
            request_id = await bhaptics_python.play_loop(event_name, 5.0, 1.0, 0.0, 0.0, 1000, 10)
            print(f"{event_name} play_loop request_id {request_id}")
        elif user_input == 'result':
            await bhaptics_python.play_without_result(event_name, 5.0, 1.0, 0.0, 0.0)
            print(f"{event_name} play_without_result")
        elif user_input == 'ppp':
            request_id = await bhaptics_python.play_param(event_name, 5.0, 1.0, 0.0, 0.0)
            print(f"{event_name} play_position_with_parameter request_id {request_id}")
        elif user_input == 'loopd':
            request_id = await bhaptics_python.play_loop(event_name, 5.0, 1.0, 0.0, 0.0, 1000, 10, device_index)
            print(f"{event_name} play_loop request_id {request_id}")
        elif user_input == 'resultd':
            await bhaptics_python.play_without_result(event_name, 5.0, 1.0, 0.0, 0.0, device_index)
            print(f"{event_name} play_without_result")
        elif user_input == 'pppd':
            request_id = await bhaptics_python.play_param(event_name, 5.0, 1.0, 0.0, 0.0, device_index)
            print(f"{event_name} play_position_with_parameter request_id {request_id}")
        elif user_input == 'retry':
            await bhaptics_python.retry_initialize(app_id, api_key)
        elif user_input == 'is':
            print(f"is_connected {await bhaptics_python.is_connected()}")
        elif user_input == 'close':
            await bhaptics_python.close()
        elif user_input == 'running':
            print(f"is_bhaptics_player_running {await bhaptics_python.is_bhaptics_player_running()}")
        elif user_input == 'install':
            print(f"is_bhaptics_player_installed {await bhaptics_python.is_bhaptics_player_installed()}")
        elif user_input == 'runt':
            print(f"run_bhaptics_player {await bhaptics_python.run_bhaptics_player(true)}")
        elif user_input == 'runf':
            print(f"run_bhaptics_player {await bhaptics_python.run_bhaptics_player(false)}")
        else:
            # 여기에 입력값에 대한 처리를 추가할 수 있습니다.
            print(f"You entered: {user_input}")

asyncio.run(main())