# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 17:56:58 2019

@author: SSB
"""

import sys
import math

def getDistanceFromRepresentatives(point,representativePoints_shifted):
    minimumDistance=float("inf")
    for repr_point in representativePoints_shifted:
        distance=getDistance(point,repr_point)
        if distance < minimumDistance:
            minimumDistance=distance
    
    return minimumDistance


def computeCentroid(initialCluster):
    x=0
    y=0
    
    for point in initialCluster:
        x+=point[0]
        y+=point[1]
    numberOfPoints=len(initialCluster)
    
    return(x/numberOfPoints,y/numberOfPoints)


def findRepresentativePoints(initialCluster):
    representativePoints=[]
    representativePoints.append(list(initialCluster[0]))
    
    for i in range(n-1):
        maximumDistance=float("-inf")
        for point in initialCluster:
            if point in representativePoints:
                continue
            minimumDistance=float("inf")
            for representativePoint in representativePoints:
                distance=getDistance(point,representativePoint)
                if distance < minimumDistance:
                    minimumDistance=distance
                    
            if minimumDistance > maximumDistance:
                candidateRepresentativePoint = point
                maximumDistance = minimumDistance
            
        representativePoints.append(list(candidateRepresentativePoint))
    return representativePoints
    
    

def getDistance(point1, point2):
    distance = (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2
    return math.sqrt(distance)


def clusterDistance(cluster1,cluster2):
    minimumDistance = float("inf")
    for point1 in cluster1:
        for point2 in cluster2:
            if minimumDistance > getDistance(point1,point2):
                minimumDistance=getDistance(point1,point2)
                
    return minimumDistance


def formClusters_heirarchical(sampleData): 
    clusters = [[i] for i in sampleData]
    
    iters = len(sampleData) - k
    for iter in range(iters):
        min = float("inf")
        for i in range(0, len(clusters) - 1):
            for j in range(i + 1, len(clusters)):
                if min > clusterDistance(clusters[i], clusters[j]):
                    min = clusterDistance(clusters[i], clusters[j])
                    c1 = i
                    c2 = j

        clusters[c1].extend(clusters[c2])
        del clusters[c2]
    
    return clusters


sampleDataFile = open(sys.argv[1]).readlines()
completeDataFile = open(sys.argv[2]).readlines()



k=int(sys.argv[3])
n=int(sys.argv[4])
p=float(sys.argv[5])
outputFileName=sys.argv[6]


completeData =[]



for line in completeDataFile:
    line = line.split(",")
    completeData.append((float(line[0]), float(line[1])))
    
    
    
sampleData=[]

  
    
    

    
for line in sampleDataFile:
    line = line.split(",")
    sampleData.append((float(line[0]), float(line[1])))
    
sampleData=sorted(sampleData,key= lambda x: (x[0],x[1]))

initialClusters= formClusters_heirarchical(sampleData)

representativePointsList=[]
representativePoints_shifted=[]

for initialCluster in initialClusters:
    representivePoints = findRepresentativePoints(initialCluster)
    representativePointsList.append(representivePoints)
    shiftedRepresentativePoints = []
    centroid=computeCentroid(initialCluster)
    for representativePoint in representivePoints:
        shiftX= (centroid[0] - representativePoint[0]) * p
        shiftY = (centroid[1] - representativePoint[1]) * p
        shiftedRepresentativePoints.append((representativePoint[0]+shiftX,representativePoint[1]+shiftY))
    representativePoints_shifted.append(shiftedRepresentativePoints)
    
    
for representativePoint in representativePointsList:
    print(representativePoint)
    
outputPointList=[]

for point in completeData:
    minimumDistance=float("inf")
    for clusterNum in range(k):
        distance=getDistanceFromRepresentatives(point,representativePoints_shifted[clusterNum])
        if distance < minimumDistance:
            minimumDistance=distance
            clusterId=clusterNum
    outputPointList.append((point,clusterId))
    
print("outputPointList len")
print(len(outputPointList))

w = open(outputFileName,'w')

for point in outputPointList:
    w.write(str(point[0][0])+","+str(point[0][1])+","+str(point[1])+"\n")
    
w.close()


    