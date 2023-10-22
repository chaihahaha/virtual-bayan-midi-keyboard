import sys
import keyboard
import mido
import json
import argparse
from midicc2name import midicc_code_to_note_name

def create_config_generator_callback(dump_config_path):
    # use this function to generate a hook callback that generates a config json file when keyboard keys are pressed according to midicc code sequence
    midicc = [i for i in range(24, 97)]
    pressed_key = []
    config_dict = {'key_midi_map': dict(), 'output_port': 0, 'supress': True}
    def generate_config(event):
        print("event type:", event.event_type)
        if event.event_type=="up":
            print("pressed key:", event.scan_code, "is keypad?", event.is_keypad)
            print("attached note", midicc_code_to_note_name(midicc[len(pressed_key)]))
            pressed_key.append(f"{event.scan_code}-{event.is_keypad}")
        config_dict['key_midi_map'] = {key: mcode for key, mcode in zip(pressed_key, midicc)}
        with open(dump_config_path,'w') as f:
            json.dump(config_dict, f)
        return
    return generate_config

def create_play_callback(config):
    port = set_midi_output(config)
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
    if key_name == '1-False':
        # if Esc is pressed, exit program
        sys.exit()
    return midimsg

def set_midi_output(config=None):
    if config is None:
        output_port = mido.open_output()
    elif 'output_port' in config:
        if config['output_port']:
            output_port = mido.open_output(config['output_port'])
        else:
            output_port = mido.open_output()
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

def run():
    parser = argparse.ArgumentParser(description='terminal virtual piano')
    parser.add_argument('-c', '--load_config_path', default='./compact_bayan_config.json', help='config json file path')
    parser.add_argument('-d', '--dump_config_path', help='config json file path')
    parser.add_argument('-g', '--generate_config', default=False, action='store_true', help='interactively generate config json file')
    args = parser.parse_args()
    if args.generate_config:
        keyboard.hook(create_config_generator_callback(args.dump_config_path), suppress=True)
        keyboard.wait()
    elif args.load_config_path:
        config = read_config(args.load_config_path)
        keyboard.hook(create_play_callback(config), suppress=config['supress'])
        keyboard.wait()

if __name__ == '__main__':
    run()
