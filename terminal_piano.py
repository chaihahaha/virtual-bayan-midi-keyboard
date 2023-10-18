import keyboard
import mido
import json
import argparse

def create_generate_config_callback():
    # use this function to generate a hook callback that generates a config json file when keyboard keys are pressed according to midicc code sequence
    midicc = [i for i in range(24, 97)]
    pressed_key = []
    config_dict = {'key_midi_map': dict(), 'output_port': 0, 'supress': True}
    def generate_config(event):
        print(event.event_type)
        if event.event_type=="up":
            print(event.scan_code)
            print(event.is_keypad)
            pressed_key.append(f"{event.scan_code}-{event.is_keypad}")
        config_dict['key_midi_map'] = {key: mcode for key, mcode in zip(pressed_key, midicc)}
        with open('normal_config.json','w') as f:
            json.dump(config_dict, f)
        return
    return generate_config

def create_callback(config):
    port = set_midi_output()
    existing_onmsg_list = [None for i in range(256)]
    def play_midi(event):
        midimsg = kbevent_to_midimsg(config, event, existing_onmsg_list)
        send_midi_message_to_output_port(port, midimsg)
        return
    return play_midi

def kbevent_to_midimsg(config, event, existing_onmsg_list):
    key_name = f"{event.scan_code}-{event.is_keypad}"
    midimsg = None
    if key_name in config['key_midi_map']:
        midicc = config['key_midi_map'][key_name]
        updown2onoff = {'up': 'off', 'down': 'on'}
        onoff = updown2onoff[event.event_type]
        msg = mido.Message(f'note_{onoff}', note=midicc, velocity=90)
        if onoff == "on" and existing_onmsg_list[midicc] is None:
            midimsg = msg
            existing_onmsg_list[midicc] = midimsg
            return midimsg
        if onoff == "off" and existing_onmsg_list[midicc] is not None:
            midimsg = msg
            existing_onmsg_list[midicc] = None
            return midimsg
    return midimsg

def set_midi_output(config=None):
    if config is None:
        output_port = mido.open_output()
    else:
        output_port = mido.open_output(config['output_port'])
    return output_port

def send_midi_message_to_output_port(port, midimsg):
    if midimsg is None:
        return
    else:
        port.send(midimsg)
    return

def read_config(filename):
    with open(filename, "r") as f:
        return json.load(f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='terminal virtual piano')
    parser.add_argument('config_path', help='config json file path')
    args = parser.parse_args()
    config = read_config(args.config_path)
    keyboard.hook(create_callback(config), suppress=config['supress'])
    keyboard.wait()
