- [NI-DAQ USB 6349 specifications](../usb-6349_specifications_usb-6349_specifications_2026-04-01-11-37-14.pdf)

  - APFI 0: Start Trigger, Reference Trigger, Pause Trigger, Sample Clock, Sample Clock Timebase

  - PFI: Counter/Timer Signal

  - AI Input range ±1 V, ±2 V, ±5 V, ±10 V

  - NI-DAQ USB 6349: AI only supports differential inputs (AI+ vs AI-), no RSE (signle ended support)

  - sample clock: is the onboard (i.e integrated inside the NI-DAQ USB 6349) clock

  - NI-DAQ USB 6349 (simultaneous sampling on all AI channels): max 500k S/s

- NI-DAQ manual: `../370784k.pdf`

- **To connect/address the right NI-USB device correctly in the code**, at code lines such as 

```
(cont_gen_voltage_wfm_int_clk.py)
        task.ao_channels.add_ao_voltage_chan("Dev2/ao0", min_val=-5.0, max_val=5.0)
        task.ao_channels.add_ao_voltage_chan("Dev2/ao1", min_val=-5.0, max_val=5.0)
```

**The `<NI_USB_DEVICE>`** in `<NI_USB_DEVICE>/ao0` or `<NI_USB_DEVICE>/ao1` **must match the device name detected by NI_MAX** software: **open NI_MAX** -> **Devices and Interfaces** -> **check the detected NI-USB device, such as NI USB-6353 "Dev2"** -> the **`<NI_USB_DEVICE>` = `Dev2`**, otherwise ERROR that the device is not detected/ without power/ damaged.    

- t**he NI-USB device can be controlled by multiple sections**: for example, a terminal runs python code for generating voltage at AOs of NI-MAX, at the same time, another terminal runs python code for acquiring the voltage at AIs.

- Meaning of **Digital lines in NI-USB devices** (see [the document](../usb-6501_user_manual_using_the_digital_input_output_lines_2026-04-01-11-30-42.pdf)):

  - for example of [NI-USB 6349](../usb-6349_specifications_usb-6349_specifications_2026-04-01-11-37-14.pdf), it has 1 digital i/o port: P0. In this port P0, it has 8 digital lines P0<0>, P0<1>, .. P0<7>. In code, we could create a output digital port linked to P0, which then is configure to control only one digital line of either the P0<0> or P<1>.. or P<7> or to control a group of digital line in the port such as P<0> & P<1>; or P<0> & P<1> & P<2>; etc. The [example code](../references/write_dig_lines.py) is following 

  ```
  # Case 1: 1 output digital port control only 1 digital line:  
    //      output constant logic 1 (= +5V) on line 0 of P0: P0<0>
    data = [True]
    task.do_channels.add_do_chan("Dev1/port0/line0", line_grouping=LineGrouping.CHAN_PER_LINE)
  
  # Case 2: 1 output digital port control a group of digital lines:
    //      constant logic 0 (=0V) on P0<0>, constant logic 1 (=+5V) on P<1>
    data = [False, True]
    task.do_channels.add_do_chan("Dev1/port0/line0:1", line_grouping=LineGrouping.CHAN_PER_LINE)
    
  ``` 

    - [example code of create a digital output port controlling all of the lines in the port](../references/write_dig_port.py): = controll all P0<i> (i=0..7) in port P0

- Example of: [digital output - using internal clock signal with configured rate - control 1 line of digital port](../references/gen_dig_line_int_clk.py)

  - by default, 1 digital sample is output/generated at the rising edge of the internal clock. Therefore, 1 digital sample duration = 1 period of the internal clock. for example of the code below

```
# gen_dig_line_int_clk.py

# the code below output a digital waveform of total duration = 1/clock_rate * number_of_digital_samples = (1 /100) * 4 = 40 ms.
# Each digital samples specified in `data` (i.e `True` or `False`) lasts for (1/clock_rate = 1/100) 10ms. 
# `True` = logic 1 = +5V
# `False` = logic 0 = 0V
    data = [True, False, True, False]

    task.do_channels.add_do_chan("Dev1/port0/line0", line_grouping=LineGrouping.CHAN_PER_LINE)
    task.timing.cfg_samp_clk_timing(
        100.0, sample_mode=AcquisitionType.FINITE, samps_per_chan=len(data)
    )
``` 
  

