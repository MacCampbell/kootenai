#!/usr/bin/env python3
# GTseq_SummaryFigures_v3_Tetra.py
# by Nate Campbell
# produce summary figures for GTseq libraries using GTseq_Genotyper_v3 output formatted files.
# Also outputs summary data in text format for further analysis.

import math
from os import listdir
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

print('type the path to directory containing .genos files for library *use single quotes*\nFormat= \'/home/user/...\'')
path = input()

print('type the library name *use single quotes*')
Lname = input()

fout_name = Lname + '_SummaryData.txt'
f_out = open(fout_name, 'w')
f_out.write(Lname)
f_out.write('GTseq Summary Data\n\n')

list1 = listdir( path )
flist = []
assaylist = []

#filter for .genos files in directory and add to "flist"...
for i in list1:
 if '.genos' in i:
  j = path + '/' + i
  flist.append(j)

#open top file and create assay list...initialize dictionary of loci with their corresponding percentage of on-target reads
OT_Dict = {}
StDEV_Dict = {}
OTP_Dict = {}
StDEV2_Dict = {}
f = open(flist[0])
lineNo = 0
for line in f:
 lineNo = lineNo + 1
 if lineNo > 1:
  stuff = line.split(',')
  assaylist.append(stuff[0])
  OT_Dict[stuff[0]] = float(0)
  StDEV_Dict[stuff[0]] = float(0)
  OTP_Dict[stuff[0]] = float(0)
  StDEV2_Dict[stuff[0]] = float(0)

f.close()

#Initialize variables...
AssayNum = float(len(assaylist))
xmax = 0
xmax2 = 0
num90 = float(0)
per90 = float(0)
inds = float(len(flist))
aveOTP = float(0)

AssayNum = float(len(assaylist))
inds = float(len(flist))

for loci in assaylist:
 for genos in flist:
  g = open(genos)
  for line in g:
   info = line.split(',')
   if loci in info[0] and len(info[0]) == len(loci):
    OT_Dict[info[0]] = OT_Dict[info[0]] + float(info[10])
    OTP_Dict[info[0]] = OTP_Dict[info[0]] + float(info[9])

#Get the mean of percenage of OT reads for each locus and mean of percentage
#forward primer reads containing probe sequences for each locus...
for loci in assaylist:
 OT_Dict[loci] = OT_Dict[loci] / inds
 OTP_Dict[loci] = OTP_Dict[loci] / inds

#Calculate standard deviations at each locus...
for loci in assaylist:
 for genos in flist:
  g = open(genos)
  for line in g:
   info = line.split(',')
   if loci in info[0] and len(info[0]) == len(loci):
    variance = (float(info[10]) - OT_Dict[loci])**2
    variance2 = (float(info[9]) - OTP_Dict[loci])**2
    StDEV_Dict[loci] = StDEV_Dict[loci] + variance
    StDEV2_Dict[loci] = StDEV2_Dict[loci] + variance2
    

for loci in assaylist:
 StDEV_Dict[loci] = (math.sqrt(StDEV_Dict[loci] / inds))
 StDEV2_Dict[loci] = (math.sqrt(StDEV2_Dict[loci] / inds))

#plot read distribution bar graph using means and standard deviation for each locus...
plt.figure()
sp1 = plt.subplot(221)  #working on this...
sp2 = plt.subplot(222)
sp3 = plt.subplot(223)
sp4 = plt.subplot(224)
bar_width = 1
opacity = 0.4
left = 0
L_AvOTP = 100 / AssayNum

print('Read Distribution data (sorted by locus name)\n')
f_out.write('Read Distribution data (sorted by locus name)\n')
for loci in assaylist:
 sp1.bar(left, OT_Dict[loci], width=bar_width, bottom=None, 
 edgecolor='b', yerr=StDEV_Dict[loci], color='b', error_kw=dict(ecolor='black', lw=0.5, alpha=0.5, capsize=0.5))
 print(loci, OT_Dict[loci], StDEV_Dict[loci])
 f_out.write(loci + '\t' + str(OT_Dict[loci]) + '\t' + str(StDEV_Dict[loci]) + '\n')
 left = left + bar_width

sp1.plot([0, left], [L_AvOTP, L_AvOTP], 'r-', linewidth=1.0)
#sp1.set_xlabel('Loci')
sp1.set_ylabel('% of On-Target Reads')
sp1.title.set_text('Read distribution (unsorted)')

Sorted_OT = sorted(OT_Dict.values())
Sorted_OTkeys = sorted(OT_Dict, key=OT_Dict.get)
Sorted_stDEV = []
Sorted_OTP = sorted(OTP_Dict.values())
Sorted_OTPkeys = sorted(OTP_Dict, key=OTP_Dict.get)
Sorted_stDEV2 = []

#Get sorted list of standard deviations for error bars...
for loci in Sorted_OTkeys:
 Sorted_stDEV.append(StDEV_Dict[loci])
for loci in Sorted_OTPkeys:
 Sorted_stDEV2.append(StDEV2_Dict[loci])

print('Read Distribution data (sorted by value)\n')
f_out.write('\nRead Distribution data (sorted by value)\n')
#populate read distribution bar graph using sorted data...
left = 0
Assays = int(AssayNum)
for x in range(0, Assays):
 sp2.bar(left, Sorted_OT[x], width=bar_width, bottom=None,
 edgecolor='green', yerr=Sorted_stDEV[x], color='green', error_kw=dict(ecolor='black', lw=0.5, alpha=0.5, capsize=0.5))
 print(Sorted_OTkeys[x], Sorted_OT[x], Sorted_stDEV[x])
 f_out.write(Sorted_OTkeys[x] + '\t' + str(Sorted_OT[x]) + '\t' + str(Sorted_stDEV[x]) + '\n')
 left = left + bar_width

sp2.plot([0, left], [L_AvOTP, L_AvOTP], 'r-', linewidth=1.0)
#plt.xlabel('Loci')
sp2.title.set_text('Read distribution (Sorted)')

print('Primer Reads On-Target (reads with forward primer AND probe / reads with fwd primer)*100\n')
f_out.write('\nPrimer Reads On-Target (reads with forward primer AND probe / reads with fwd primer)*100\n')
#Create bar graph of percentage (reads with forward primer AND probe / reads with fwd primer)...
left = 0
for loci in assaylist:
 sp3.bar(left, OTP_Dict[loci], width=bar_width, bottom=None,
 edgecolor='b', yerr=StDEV2_Dict[loci], color='b', error_kw=dict(ecolor='black', lw=0.5,
 alpha=0.5, capsize=0.5))
 print(loci, OTP_Dict[loci], StDEV2_Dict[loci])
 f_out.write(loci + '\t' + str(OTP_Dict[loci]) + '\t' + str(StDEV2_Dict[loci]) + '\n')
 left = left + bar_width

sp3.set_xlabel('Loci')
sp3.set_ylabel('% On-Target Primers')
sp3.title.set_text('Primers On-Target (unsorted)')

print('Primer Reads On-Target (sorted) (reads with forward primer AND probe / reads with fwd primer)*100\n')
f_out.write('\nPrimer Reads On-Target (sorted) (reads with forward primer AND probe / reads with fwd primer)*100\n')
#Create sorted bar graph of percentage (reads with forward primer AND probe / reads with fwd primer)...
left = 0
for x in range(0, Assays):
 sp4.bar(left, Sorted_OTP[x], width=bar_width, bottom=None,
 color='red', edgecolor='red', yerr=Sorted_stDEV2[x], error_kw=dict(ecolor='black', lw=0.5, 
 alpha=0.5, capsize=0.5))
 print(Sorted_OTPkeys[x], Sorted_OTP[x], Sorted_stDEV2[x])
 f_out.write(Sorted_OTPkeys[x] + '\t' + str(Sorted_OTP[x]) + '\t' + str(Sorted_stDEV2[x]) + '\n')
 left = left + bar_width

sp4.set_xlabel('Loci')
sp4.title.set_text('Primers On-Target (sorted)')
#plt.figure(2)
plt.suptitle(Lname, fontsize=16)
plt.subplots_adjust(top=0.9, wspace=0.3, hspace=0.4)
plt.savefig(Lname + '_001.png', dpi=300, format='png')
plt.clf()

print('Library Summary\n')
f_out.write('\nLibrary Summary\n')
#open each .genos file and define x and y coordinates for plotting Raw-reads vs. GT% graph...

plt.figure()  # open figure for matplotlib...
sub1 = plt.subplot(2,2,1)  # declare subplot 1
sub2 = plt.subplot(2,2,2)  # declare subplot 2
sub3 = plt.subplot(2,2,3)  # declare subplot 3
sub4 = plt.subplot(2,2,4)  # declare subplot 4

for genos in flist:
 g = open(genos)
 genper = float(0)
 otreads = 0
 rawreads = 0
 NA = 0
 lineNo2 = 0
 for line in g:
  lineNo2 = lineNo2 + 1
  if lineNo2 == 1:
   info = line.split(',')
   RRarr = info[1].split(':')
   OTarr = info[2].split(':')
   OTParr = info[3].split(':')
   otreads = int(OTarr[1])/1000
   rawreads = int(RRarr[1])/1000
   aveOTP = aveOTP + float(OTParr[1])
  elif lineNo2 > 1:
   info2 = line.split(',')
   if 'NA' in info2[5]:
    NA = NA + 1
 if rawreads > xmax:
  xmax = rawreads
 if otreads > xmax2:
  xmax2 = otreads
 NA = float(NA)
 genper = (1 - (NA / AssayNum)) * 100
 scale = 50.0
 if genper >= 90:
  num90 = num90 + 1
 #print(genos,otreads,genper)
 sub1.scatter(rawreads, genper, c='orange', s=scale, label='black',alpha=0.4, edgecolors='none')
 sub2.scatter(otreads, genper, c='black', s=scale, label='black',alpha=0.4, edgecolors='none')
per90 = num90 / inds * 100
aveOTP = aveOTP / inds

perSTR = str(per90)
aveOTPSTR = str(aveOTP)

text1 = 'Samples in library: ' + str(int(inds))
text2 = 'Samples over 90% GT: ' + str(int(num90))
text3 = 'Percentage over 90% GT: ' + perSTR[:4] + '%'
text4 = 'Average OT-Percentage: ' + aveOTPSTR[:4] + '%'
print(text1, text2, text3, text4)
f_out.write(text1 + '\n')
f_out.write(text2 + '\n')
f_out.write(text3 + '\n')
f_out.write(text4 + '\n')

font = {'family' : 'serif',
 'color'  : 'darkred',
 'weight' : 'normal',
 'size'   : 10,
 }

#plt.subplot(221)
sub1.plot([0, xmax], [90, 90], 'r-', linewidth=2.0)
sub1.grid(True)
sub1.axis([-5, xmax, -5, 105])
sub1.title.set_text('Raw Reads (K)')
sub1.set_ylabel('Genotyping Percentage')
sub1.text(25, 50, text1, fontdict=font)
sub1.text(25, 40, text2, fontdict=font)
sub1.text(25, 30, text3, fontdict=font)
sub1.text(25, 20, text4, fontdict=font)

#plt.subplot(222)
sub2.plot([0, xmax2], [90, 90], 'r-', linewidth=2.0)
sub2.grid(True)
sub2.axis([-5, xmax2, -5, 105])
sub2.title.set_text('On-Target Reads (K)')
#sub2.set_ylabel('Genotyping Percentage')
sub2.text(25, 50, text1, fontdict=font)
sub2.text(25, 40, text2, fontdict=font)
sub2.text(25, 30, text3, fontdict=font)
sub2.text(25, 20, text4, fontdict=font)

print('Per-locus Summary\n')
f_out.write('\nPer-locus Summary\n')

#Gather data from all or first 100 .genos files and plot data from all loci onto a single graph...
end = 100
if inds < 100:
 end = int(inds)
print('Plotting all loci for %s samples...\nKeepin it 100...\nLots of data points\nThis will take a couple minutes\n' % end)
for i in range(0, end):

 lineNo = 0
 g = open(flist[i])
 for line in g:
  lineNo = lineNo + 1
  if lineNo > 1:
   info = line.split(',')
   xarr = info[1].split('=')
   yarr = info[2].split('=')
   x = int(round(float(xarr[1])))
   y = int(round(float(yarr[1])))
   ratio = float(info[3])
   sum_xy = x + y
   scale = 30.0
   if sum_xy < 20:
    color = 'black'
   elif sum_xy == 0:
    color = 'black'
   elif ratio >= 19:
    color = 'red'
   elif ratio > 5.666:
    color = 'gray'
   elif ratio > 1.85:
    color = 'orange'
   elif ratio > 1.5:
    color = 'gray'
   elif ratio > 0.666:
    color = 'yellow'
   elif ratio > 0.538:
    color = 'gray'
   elif ratio > 0.176:
    color = 'green'
   elif ratio > 0.0526:
    color = 'gray'
   elif ratio <= 0.0526:
    color = 'blue'
   else:
    color = 'gray'
   #plt.subplot(223)
   sub3.scatter(x, y, c='none', s=scale, label=color,alpha=0.4, edgecolors=color)
   #plt.subplot(224)
   sub4.scatter(x, y, c='none', s=scale, label=color,alpha=0.4, edgecolors=color)

#plt.subplot(223)
sub3.grid(True)
plt.axis([-5, 500, -5, 500])
#plt.plot([0, 10], [10, 0], 'y-', linewidth=2.0)
#plt.plot([9, 10000], [1, 1000], 'r-', linewidth=2.0)
#plt.plot([1000, 1], [10000, 9], 'b-', linewidth=2.0)
#plt.plot([5, 10000], [5, 10000], 'm-', linewidth=2.0)
#plt.plot([6.6, 10000], [3.3, 5000], 'k-', linewidth=2.0)
#plt.plot([3.3, 5000], [6.6, 10000], 'k-', linewidth=2.0)
#sub3.title.set_text('Taste the Rainbow!')
sub3.set_xlabel('A1 counts')
sub3.set_ylabel('A2 counts')

#plt.subplot(224)
plt.grid(True)
plt.axis([-5, 100, -5, 100])
#plt.plot([0, 40], [40, 0], 'y-', linewidth=2.0)
#plt.plot([9, 10000], [1, 1000], 'r-', linewidth=2.0)
#plt.plot([1000, 1], [10000, 9], 'b-', linewidth=2.0)
#plt.plot([5, 10000], [5, 10000], 'm-', linewidth=2.0)
#plt.plot([6.6, 10000], [3.3, 5000], 'k-', linewidth=2.0)
#plt.plot([3.3, 5000], [6.6, 10000], 'k-', linewidth=2.0)
#sub4.title.set_text('Taste the Rainbow (Zoom)')
sub4.set_xlabel('A1 counts')
#sub4.set_ylabel('A2 counts')
#plt.figure(1)
plt.suptitle(Lname, fontsize=16)
plt.savefig(Lname + '_002.png', dpi=300, format='png')
plt.clf()

print('Done...\n\nNow creating plots for each locus...\n')

#Create summary data for each locus including allele counts scatter plot, allele frequency scatter plot, % of OT reads bar graph
#with locus bar highlighted, and % of reads on target with locus bar highlighted...
fig_num = 2
for loci in assaylist:
 plt.figure()  #declare figure
 sb1 = plt.subplot(221)  #declare subplots ...
 sb2 = plt.subplot(222)
 sb3 = plt.subplot(223)
 sb4 = plt.subplot(224)
 fig_num = fig_num + 1
 str_fig_num = 0
 if len(str(fig_num)) == 1:
  str_fig_num = '00' + str(fig_num)
 elif len(str(fig_num)) == 2:
  str_fig_num = '0' + str(fig_num)
 else:
  str_fig_num = str(fig_num)
 xmax = 0
 ymax = 0
 fmax = 0
 fmax2 = 0
 A1_corr = float(0)
 A2_corr = float(0)
 gt_per = float(0)
 gt_inds = float(0)
 inds = float(len(flist))
 for genos in flist:
  g = open(genos)
  for line in g:
   info = line.split(',')
   if loci in info[0] and len(info[0]) == len(loci):
    size = len(info)
    if size == 13:
     A1_corr = float(info[6])
     A2_corr = float(info[7])
    xarr = info[1].split('=')
    yarr = info[2].split('=')
    x = int(round(float(xarr[1])))
    y = int(round(float(yarr[1])))
    ratio = float(info[3])
    sum_xy = x + y
    AF_div = float(xarr[1]) + float(yarr[1])
    if AF_div == 0:
     AF_div = 0.1
    p_A2 = float(yarr[1])/AF_div*100
    scale = 50.0
    if x > xmax:
     xmax = x
    if y > ymax:
     ymax = y
    if sum_xy > fmax2:
     fmax2 = sum_xy
    if sum_xy < 20:
     color = 'black'
    elif sum_xy == 0:
     color = 'black'
    elif ratio >= 19:
     color = 'red'
     gt_inds = gt_inds + 1
    elif ratio > 5.666:
     color = 'gray'
    elif ratio > 1.85:
     color = 'orange'
     gt_inds = gt_inds + 1
    elif ratio > 1.5:
     color = 'gray'
    elif ratio > 0.666:
     color = 'yellow'
     gt_inds = gt_inds + 1
    elif ratio > 0.538:
     color = 'gray'
    elif ratio > 0.176:
     color = 'green'
     gt_inds = gt_inds + 1
    elif ratio > 0.0526:
     color = 'gray'
    elif ratio <= 0.0526:
     color = 'blue'
     gt_inds = gt_inds + 1
    else:
     color = 'gray'
    #plt.subplot(221)
    sb1.scatter(x, y, c=color, s=scale, label=color,alpha=0.4, edgecolors='none')
    #plt.subplot(222)
    sb2.scatter(sum_xy, p_A2, c=color, s=scale, label=color,alpha=0.4, edgecolors='none')
 if xmax > ymax:
  fmax = xmax
 else:
  fmax = ymax
 gt_per = gt_inds / inds * 100
 gt_per = str(gt_per)
 A1_corr = str(A1_corr)
 A2_corr = str(A2_corr)
 text = ' : Corrections [' + A1_corr[:3] + ', ' + A2_corr[:3] + '] : GT% = ' + gt_per[:5]
 print(loci + text)
 f_out.write(loci + text + '\n')
 #Create first subplot XY scatter A1 vs A2 counts...
 #plt.subplot(221)
 sb1.grid(True)
 sb1.axis([-5, fmax, -5, fmax])
 #plt.plot([0, 10], [10, 0], 'y-', linewidth=2.0)
 #plt.plot([9, 10000], [1, 1000], 'r-', linewidth=2.0)
 #plt.plot([1000, 1], [10000, 9], 'b-', linewidth=2.0)
 #plt.plot([5, 10000], [5, 10000], 'm-', linewidth=2.0)
 #plt.plot([6.6, 10000], [3.3, 5000], 'k-', linewidth=2.0)
 #plt.plot([3.3, 5000], [6.6, 10000], 'k-', linewidth=2.0)
 sb1.title.set_text('A1 vs A2 counts')
 #sb1.set_xlabel('A1 counts')
 sb1.set_ylabel('A2 counts')
 
 #Create second suplot % A2 counts...
 #plt.subplot(222)
 sb2.grid(True)
 sb2.axis([-5, fmax2, -5, 105])
 #plt.plot([10, 10], [0, 100], 'y-', linewidth=2.0)
 #plt.plot([0, 10000], [10, 10], 'r-', linewidth=2.0)
 #plt.plot([0, 10000], [90, 90], 'b-', linewidth=2.0)
 #plt.plot([10, 10000], [66.6, 66.6], 'k-', linewidth=2.0)
 #plt.plot([10, 10000], [33.3, 33.3], 'k-', linewidth=2.0)
 sb2.title.set_text('% allele 2')
 #sb2.set_xlabel('Counts')
 sb2.set_ylabel('% A2 counts')
 
 #continue with bar graph subplots...
 #plt.subplot(223)
 left = 0
 for x in range(0, Assays):
  bar_color='grey'
  ebar_color='grey'
  opacity=0.5
  if loci in Sorted_OTkeys[x] and len(loci) == len(Sorted_OTkeys[x]):
   bar_color='red'
   ebar_color='black'
   opacity=1
   text = text + '\nPercentage of On-Target Reads = ' + str(Sorted_OT[x])[:4]
  sb3.bar(left, Sorted_OT[x], width=bar_width, bottom=None, 
  alpha=opacity, yerr=Sorted_stDEV[x], color=bar_color, edgecolor=bar_color,
  error_kw=dict(ecolor=ebar_color, lw=0.5, alpha=opacity, capsize=0.5))
  left = left + bar_width

 sb3.plot([0, left], [L_AvOTP, L_AvOTP], 'r-', linewidth=1.0)
 sb3.set_xlabel('Loci')
 sb3.set_ylabel('Percentage of On-Target Reads')
 #sb3.title.set_text('Read distribution among loci')
 
 #plt.subplot(224)
 left = 0
 for x in range(0, Assays):
  bar_color='grey'
  ebar_color='grey'
  opacity=0.5
  if loci in Sorted_OTPkeys[x] and len(loci) == len(Sorted_OTPkeys[x]):
   bar_color='red'
   ebar_color='black'
   opacity=1
   text = text + '\nOn-target Primer = ' + str(Sorted_OTP[x])[:4]
  sb4.bar(left, Sorted_OTP[x], width=bar_width, bottom=None,
  alpha=opacity, yerr=Sorted_stDEV2[x], color=bar_color, edgecolor=bar_color,
  error_kw=dict(ecolor=ebar_color, lw=0.5, alpha=opacity, capsize=0.5))
  left = left + bar_width

 sb4.set_xlabel('Loci')
 sb4.set_ylabel('Percentage On-Target Primers')
 #sb4.title.set_text('Primers On-Target')
 
 plt.suptitle(loci + text, fontsize=16)
 plt.subplots_adjust(top=0.8, wspace=0.3, hspace=0.4)
 plt.savefig(Lname + '_' + str_fig_num + '.png', format='png', dpi=300)
 plt.clf()

f_out.close()
summary = 'All done.\nSummary data: %s\nSummary figures: are saved in the current folder'
print(summary % (fout_name))
print('Convert figures to .pdf using the convert command **$ convert *png LXXXX.pdf**')

