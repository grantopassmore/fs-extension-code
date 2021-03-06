#!/usr/bin/env python 
import sys
import subprocess
import math
import re
import os.path

# directory of scripts
scriptsDir = "scripts"
sys.path.append(scriptsDir)
# directory of models
modelDir = os.path.join("..", "models", "bench")

import my_functions as fs

pairs = []

pairs = pairs + [('moore_rot_plain.model', 'moore_rot_sw_10.model')]

pairs = pairs + [('vanderpol_plain.model', 'vanderpol_sw_10.model')]
pairs = pairs + [('Brusselator_plain.model', 'Brusselator_sw_10.model')]
pairs = pairs + [('jet_engine_plain.model', 'jet_engine_sw_10.model')]
pairs = pairs + [('buckling_column_plain.model', 'buckling_column_sw_10.model')]
pairs = pairs + [('Lotka_Volterra_plain.model', 'Lotka_Volterra_sw_10.model')]
pairs = pairs + [('Lorentz_plain.model', 'Lorentz_sw_10.model')]
pairs = pairs + [('Roessler_plain.model', 'Roessler_sw_10.model')]

#slow
pairs = pairs + [('biology_I_plain.model', 'biology_I_sw_10.model')]
pairs = pairs + [('biology_II_plain.model', 'biology_II_sw_10.model')]

#non poly
pairs = pairs + [('lacoperon_plain.model', 'lacoperon_sw_10.model')]
pairs = pairs + [('coupledVanderPol_plain.model', 'coupledVanderPol_sw_10.model')]

#non lin hybrid
pairs = pairs + [('nonholonomic_plain.model', 'nonholonomic_sw_10.model')]
pairs = pairs + [('neuron_I_plain.model', 'neuron_I_sw_10.model')]
pairs = pairs + [('neuron_II_plain.model', 'neuron_II_sw_10.model')]
pairs = pairs + [('diabetic_1_plain.model', 'diabetic_1_sw_10.model')]
pairs = pairs + [('diabetic_2_plain.model', 'diabetic_2_sw_10.model')]

#lin hybrid
pairs = pairs + [('bouncing_ball_plain.model', 'bouncing_ball_sw_10.model')]
pairs = pairs + [('two_tanks_plain.model', 'two_tanks_sw_10.model')]
pairs = pairs + [('rod_reactor_plain.model', 'rod_reactor_sw_10.model')]
pairs = pairs + [('cruise_control_plain.model', 'cruise_control_sw_10.model')]
pairs = pairs + [('switching_5_plain.model', 'switching_5_sw_10.model')]
pairs = pairs + [('vehicle_platoon_3_plain.model', 'vehicle_platoon_3_sw_10.model')]
pairs = pairs + [('filtered_oscillator_4_plain.model', 'filtered_oscillator_4_sw_10.model')]
pairs = pairs + [('filtered_oscillator_8_plain.model', 'filtered_oscillator_8_sw_10.model')]
pairs = pairs + [('filtered_oscillator_16_plain.model', 'filtered_oscillator_16_sw_10.model')]
pairs = pairs + [('filtered_oscillator_32_plain.model', 'filtered_oscillator_32_sw_10.model')]

def getParam(filename, param):
  with open(filename) as f:
    for line in f:
      #print line,
      m = re.search('%s (.*)' %param, line)
      if m != None:
        return m.group(1)

def getVarRange(modelFile, plain, sw):
  time = fs.find_max_time(plainCSV,swCSV)
  dim = len(getParam(modelFile, "state var").split(','))
  if not os.path.isfile(plain):
    return [-1,-1]
  if not os.path.isfile(sw):
    return [-1,-1]
  
  plainRange = swRange = []
  with open(plain) as f:
    for line in f:
      data = line.split(',')
      if float(data[0]) == float(time):
        plainRange = map(lambda x: float(x), data[2 + 2*dim: 2 + 3*dim])
  with open(sw) as f:
    for line in f:
      data = line.split(',')
      if float(data[0]) == float(time):
        #skip time, lower bounds and upper bounds
        swRange = map(lambda x: float(x), data[2 + 2*dim: 2 + 3*dim])

  #print plainRange
  #print swRange        
  zipped = zip(plainRange, swRange)
  marked = map(lambda (p,s): (p, "<b>%s</b>"%s) if (p > s) else (p,s), zipped)
        
  return (map(lambda (f,s): f, marked), map(lambda (f,s): s, marked))

def writeData(modelFile, modelName, outFile, varRange):
  if os.path.isfile(modelFile):
    infoFile = "infos/%s.txt" %getParam(modelFile, "output")
    order = getParam(modelFile, "fixed orders")
    step = getParam(modelFile, "fixed steps")
    time = getParam(modelFile, "time")
    dim = len(getParam(modelFile, "state var").split(','))
  else:
    infoFile = order = time = step = dim = '-'
  
  if os.path.isfile(infoFile):
    reason = getParam(infoFile, "reason:")
    intTime = getParam(infoFile, "integration time:")
    compTime = getParam(infoFile, "computation time:")
    swTime = getParam(infoFile, "shrink wrapping time:")
  else:
    reason = intTime = compTime = swTime = varRange = '-'
  outFile.write("  <tr>\n")
  outFile.write("    <td><a href='%s'>%s</a></td>\n"%(modelFile,modelName))
  outFile.write("    <td>%s</td> \n"%dim)
  outFile.write("    <td>%s</td>\n"%order)
  outFile.write("    <td>%s</td>\n"%step)
  outFile.write("    <td>%s</td>\n"%time)
  outFile.write("    <td>%s</td>\n"%intTime)
  outFile.write("    <td>%s</td>\n"%compTime)
  outFile.write("    <td>%s</td>\n"%swTime)
  outFile.write("    <td>%s</td>\n"%reason)
  outFile.write("    <td>%s</td>\n"%str(varRange))
  outFile.write("  </tr>\n")
  

outFile = open("experiments.html", 'w')
outFile.write("<html>\n")
outFile.write("<body>\n")

outFile.write("<table >\n")
outFile.write("  <tr>\n")
outFile.write("    <th>Model</th>\n")
outFile.write("    <th>Dim</th> \n")
outFile.write("    <th>Order</th>\n")
outFile.write("    <th>step</th>\n")
outFile.write("    <th>Time (goal)</th>\n")
outFile.write("    <th>Time (actual)</th>\n")
outFile.write("    <th>Computation time</th>\n")
outFile.write("    <th>Shrink wrapping time</th>\n")
outFile.write("    <th>Stop reason</th>\n")
outFile.write("    <th>Variable range</th>\n")
outFile.write("  </tr>\n")


for (plain, sw) in pairs:
  plainModel = os.path.join(modelDir, plain)
  swModel = os.path.join(modelDir, sw)
  
  plainCSV = os.path.join("csvs", "%s.csv" %getParam(plainModel, "output"))
  swCSV = os.path.join("csvs", "%s.csv" %getParam(swModel, "output"))
  
  varRange = getVarRange(plainModel, plainCSV, swCSV)
  
  writeData(plainModel, plain, outFile, varRange[0])
  writeData(swModel, sw, outFile, varRange[1])
  
  
  outFile.write('<tr style="border-bottom:3px solid black">' + \
      '<td colspan="100%"><hr /></td></tr>\n')
    
  
  if not os.path.isfile(plainCSV) or not os.path.isfile(swCSV):
    continue
  
  p = subprocess.Popen([os.path.join(scriptsDir, 'plot_to_max_time.py'), \
      plainCSV, swCSV, 'var1=1', 'var2=0'])
  p.wait()



outFile.write("</table>\n")
outFile.write("</body>\n")
outFile.write("</html>\n")


outFile.close()













