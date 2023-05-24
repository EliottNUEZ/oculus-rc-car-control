![Ww0Xt1mAMy31Ofar0GYu8Oab0v2k0uF1XT_zTt5kPU1M8o58sT5OOXCsSxv3nNGxsG8dG4zI=w1060-fcrop64=1,00005a57ffffa5a8-k-c0xffffffff-no-nd-rj (1)](https://user-images.githubusercontent.com/1176339/155262320-ce1406f0-d35d-418e-a8b9-60b928cceeb2.jpeg)

# 🔥🔥 RASPBERRY PI PROJECTS WITH OCULUS: I HACKED AN RC Car To Drive It With VR! 🔥🔥

## YouTube Video:

[![IMAGE ALT TEXT](http://img.youtube.com/vi/MYJcSZqk_Tg/maxresdefault.jpg)](https://youtu.be/MYJcSZqk_Tg "YouTube video")

<https://youtu.be/MYJcSZqk_Tg>

## Projects breakdown

### Oculus Unity App

#### Unity instructions

##### Unity Editor Version
2021.3.8f1

Complete the Official Oculus Tutorial back to back
https://developer.oculus.com/documentation/unity/unity-gs-overview/

Open <https://github.com/security-union/oculus-rc-car-control/tree/main/VR%20Control> and make sure to Set OVRPlugin to Legacy:
<img width="100%" alt="Schermata 2022-08-31 alle 9 22 28 PM" src="https://user-images.githubusercontent.com/1176339/187812466-7089cf51-85a3-444b-92e4-cbc109dd94e0.png">

### Raspberry PI

<https://github.com/security-union/oculus-rc-car-control/tree/main/raspberry-pi>

### Protobuf

Messages used to communicate the raspberry pi with the Oculus

<https://github.com/security-union/oculus-rc-car-control/tree/main/protobuf>

## Instruction for the project

### To know

First of all, you have to know that some libraries are bound to evolve and that can generate errors during compilation. This tutorial applies an update of some libraries like Rav1e which was previously in version 0.5.1 in this project. We will use version 0.6.1 to be able to compile this project.

### To do

#### Raspberry pi :

Update and upgrade the system

<pre><code>sudo apt-get update
sudo apt-get upgrade
</code></pre>

Clone the git repository

<pre><code>sudo apt-get install git
git clone https://github.com/security-union/oculus-rc-car-control.git
</code></pre>

After you need to install cargo

<pre><code>sudo apt-get install curl
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
</code></pre>

Modify the Cargo.toml in Oculus-rc-car-control-main/raspberry-pi/video-streaming/Cargo.toml

On the line rav1e = "0.5.1" -> rav1e = "0.6.1"

Make a cargo build

<pre><code>cargo build
</code></pre>

Setup

<pre><code>cd project_path/raspberry-pi
./setup-cross-compile-raspy.sh
</code></pre>

If everything compiles correctly you can go to the dev machine part

#### Dev machine (Ubuntu 22.04 in my case) :

##### Part 1 :

Update and upgrade the system

<pre><code>sudo apt-get update
sudo apt-get upgrade
</code></pre>

Clone the git repository

<pre><code>sudo apt-get install git
git clone https://github.com/security-union/oculus-rc-car-control.git
</code></pre>

After you need to install cargo

<pre><code>sudo apt-get install curl
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
</code></pre>

Modify the Cargo.toml in Oculus-rc-car-control-main/raspberry-pi/video-streaming/Cargo.toml

On the line rav1e = "0.5.1" -> rav1e = "0.6.1"

Make a cargo build

<pre><code>cargo build
</code></pre>

Setup

<pre><code>cd project_path/raspberry-pi
./setup-cross-compile-raspy.sh
</code></pre>

Generate a ssh key

<pre><code>ssh genkey
</code></pre>

Adapt the build-raspy.sh config in project_path/rapsberry-pi

<pre><code>sudo nano build-raspy
</code></pre>

Here you need to change the raspberry-pi_username and the raspberry-pi_ip
Save and exit

Execute the build_raspy.sh file

<pre><code>./build-raspy.sh
</code></pre>

note that this file will generate 3 files and send it to your raspberry-pi using scp. It will be in /tmp

If everything compiles correctly you can go to the second part

##### part 2 :

Open 2 terminals and connect with ssh to your raspberry pi

<pre><code>ssh pi_username@pi_ip
</code></pre>

###### Option 1 :

on the first terminal:

<pre><code>cd /tmp
RUST_LOG=info FRAMERATE=30 VIDEO_WIDTH=640 VIDEO_HEIGHT=480 VIDEO_DEVICE_INDEX=0 ENCODER=MJPEG PORT=8081 ./video-streaming
</code></pre>

on the second terminal:

<pre><code>cd /tmp
RUST_LOG=debug ./servo-control-websocket | sudo python3.9 control_rc.py
</code></pre>

If it make a libc error you can go to Option 2

###### Option 2 :

<pre><code>cd oculus-rc-car-control/raspberry-pi/target/aarch64-unknown-linux-gnu/release/
RUST_LOG=info FRAMERATE=30 VIDEO_WIDTH=640 VIDEO_HEIGHT=480 VIDEO_DEVICE_INDEX=0 ENCODER=MJPEG PORT=8081 ./video-streaming
</code></pre>

on the second terminal:

<pre><code>cd oculus-rc-car-control/raspberry-pi/target/aarch64-unknown-linux-gnu/release/
RUST_LOG=debug ./servo-control-websocket | sudo python3.9 control_rc.py
</code></pre>

Now you can go to Unity part

#### Unity :

Install Unity

Import the VR Control folder in Unity and make sure that you have the good version of Unity (2021.3.8f1)

Click on Front -> default and go to inspector

On the inspector page at the end you have Stream Controller (Script) part

For the URI put : ws://raspberry-pi_ip:8081/ws
For the URI Controller put : ws://raspberry-pi_ip:9080/ws
Check the box : Is Controller

Save, Run and Enjoy it !

#### Note :

You can see that we don't use the protobuf folder in the execution of the project because this folder is only used to make modifications to the API. The file supposed to be generated by protobuf was directly added to the VR Control folder.

Also note that you may have problems with the rc-control.py script if you don't use the same engine card because the communication protocols may be different.

So we created a draft of an rc_control.py script named rc_control_2.py for the PCA 9685 engine boards which uses the i2c protocol.