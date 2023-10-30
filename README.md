# virtual-bayan-midi-keyboard
A bayan-like virtual midi keyboard which turns your computer keyboard into a 63-key piano.

### Usage

```bash
git clone https://github.com/chaihahaha/virtual-bayan-midi-keyboard
cd virtual-bayan-midi-keyboard
pip install -r requirements.txt
python terminal_piano.py -d config.json -g # If you want to generate your own key map
python terminal_piano.py -c config.json   # If you want to play with config.json
```

Then you can use your keyboard to play a bayan layout piano.

If you want to use it with the default MIDI output port, then change 'output_port' field of `config.json` to 0.

If you want to use it as a virtual MIDI input device and drive other synthesizers, the install loopMIDI and set a loopback MIDI port with `port_name_0`, then change 'output_port' of `config.json` to `port_name_0`.
