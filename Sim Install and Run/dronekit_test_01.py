from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time


#-- Connect to the vehicle
import argparse
parser = argparse.ArgumentParser(description='commands')
parser.add_argument('--connect')
args = parser.parse_args()


connection_string = args.connect




print("Connection to the vehicle on %s"%connection_string)
vehicle = connect(connection_string, wait_ready=True)


#-- Define the function for takeoff
def arm_and_takeoff(tgt_altitude):
    print("Arming motors")


    while not vehicle.is_armable:
        time.sleep(1)


    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True


    while not vehicle.armed: time.sleep(1)


    print("Takeoff")
    vehicle.simple_takeoff(tgt_altitude)
    print("Completed takeoff")


    #-- wait to reach the target altitude
    while True:
        altitude = vehicle.location.global_relative_frame.alt
        print(">> Altitude = %.1f m"%altitude)
        if altitude >= tgt_altitude -1.0:
            print("Altitude reached")
            break
        time.sleep(1)




#----- MAIN PROGRAM ----
arm_and_takeoff(55)


#-- set the default speed
vehicle.airspeed = 7


#-- Go to wp1
print ("go to wp1")
wp1 = LocationGlobalRelative(35.9872609, -95.8753037, 45)
wp2 = LocationGlobalRelative(35.9852609, -95.8773037, 65)


vehicle.simple_goto(wp1)


#--- Here you can do all your magic....
#--- All the sleep times may have to vary, depending on your machine's speed
#-- Make them long enough to get to the waypoints and hover for a short while
time.sleep(90)


print ("go to wp2")
vehicle.simple_goto(wp2)


time.sleep(90)


#--- Coming back
print("Coming back")
vehicle.mode = VehicleMode("RTL")


time.sleep(20)


#-- Close connection
print("Done!")
vehicle.close()
