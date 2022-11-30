#--------------------------------------------------------------
# final_project.py
#--------------------------------------------------------------
# Registra el ritmo cardíaco y el porcentaje de oxígeno en la sangre.
#--------------------------------------------------------------
# Universidad del Valle de Guatemala
# Programación de microprocesadores
# Autores: Erick Guerra, Herber Silva y Daniel Morales
# Vers.  1.0
#--------------------------------------------------------------

import library.max30102
import library.hrcalc
import csv
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
sensorOn = True

try:
    m = max30102.MAX30102()
except:
    sensorOn = False

counter = 0
row = 1
touchPin = 12
ledPin = 16
register = []

GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(touchPin, GPIO.IN)

while (counter < 10) and sensorOn:
    try:
        red, ir = m.read_sequential()
        hr,hrb,sp,spb = hrcalc.calc_hr_and_spo2(ir, red)
        
        if GPIO.input(touchPin) and hrb and spb:
            hr2 = 0
            sp2 = 0
            counter = 0
            GPIO.output(ledPin, GPIO.LOW)

            if(hrb == True and hr != -999):
                hr2 = int(hr)
                print("Heart Rate : ",hr2)
            if(spb == True and sp != -999):
                sp2 = int(sp)
                print("SPO2       : ",sp2)
            register.append([row,hr2,sp2])
            row += 1            
        else:
            counter += 1
            GPIO.output(ledPin, GPIO.HIGH)
            print("ADVERTENCIA: Colocar correctamente el dispositivo.")
        sleep(1)
    except IOError as e:
        sensorOn = False
        
if len(register) > 0:
    print("Generando archivo .csv ...")

    with open('final_project.csv', mode='w') as csv_file:
        fieldnames = ['ID','Heart Rate', 'Oxygen saturation']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for r in register:
            writer.writerow({'ID': r[0], 'Heart Rate': r[1], 'Oxygen saturation': r[2]})

    sleep(3)
    print("Archivo generado, fin del programa.")

elif counter >= 10:
    print("Fin del programa por inactividad.")
elif sensorOn == False:
    print("Programa terminado.")
else:
    print("Error de ejecución")
