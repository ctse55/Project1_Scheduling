import ast

'''matching takes a person's schedule and finds the availabilities with another person's schedule'''
def groupSchedule(pers1_BusySchedule, pers1_WorkingPeriod, pers2_BusySchedule, pers2_WorkingPeriod, meetingDuration):
    updateSchedule1 = updateSchedule(pers1_BusySchedule, pers1_WorkingPeriod)
    updateSchedule2 = updateSchedule(pers2_BusySchedule, pers2_WorkingPeriod)
    combSchedule = mergedSchedules(updateSchedule1, updateSchedule2)
    sortedSchedule = sort_Schedule(combSchedule)
    print(availableTime(sortedSchedule, meetingDuration))

'''
Function that takes the person's busy schedule and their working period 
and adds empty slots to see when they are unavailable 
'''
def updateSchedule(schedule, workTime):
    copy_Schedule = schedule[:]
    conversion_Schedule = workTime[:]
    
    # Updated lines below
    updatedSchedule = copy_Schedule
    convertedWorkTime = conversion_Schedule

    #update the schedule with unavailbility time and the early starting time
    updatedSchedule.insert(0, ['0:00', convertedWorkTime[0]])   #update unavailable schedules and add early morning hurs
    
    #update the schedule with unavailability and the after work hours 
    updatedSchedule.append([convertedWorkTime[1], '23:59'])     

    #return the updated list with the appended times
    return updatedSchedule                                      

'''Function that merges the two busy schedules from person 1 and 2 '''
def mergedSchedules(pers1_Schedule, pers2_Schedule):
    merged = [[0,0]]  #initialize the merging list as empty
    i,j = 0,0

    pers1_ScheduleMinutes = minuteConversion(pers1_Schedule)
    pers2_ScheduleMinutes = minuteConversion(pers2_Schedule)

    #compares the meeting times of the two persons 
    while i < len(pers1_ScheduleMinutes) and j < len(pers2_ScheduleMinutes):
        meeting1, meeting2 = pers1_ScheduleMinutes[i], pers2_ScheduleMinutes[j]
        #if the starting time of meeting 1 is before meeting 2, then it checks if 
        #meeting 1's time is after the last time added and moved into merged schedule 
        if meeting1[0] <= meeting2[0]:        
            if meeting1[1] > merged[-1][1]:
                merged.append(meeting1)
            i += 1
        else:
            if meeting2[1] > merged[-1][1]:
                merged.append(meeting2)
            j += 1
    #appends/merges meetings that are left out and is avaiable in the person's schedule 
    while i < len(pers1_ScheduleMinutes):
        meeting1 = pers1_ScheduleMinutes[i]
        if meeting1[1] > merged[-1][1]:
            merged.append(meeting1)
        i += 1
    while j < len(pers2_ScheduleMinutes):
        meeting2 = pers2_ScheduleMinutes[j]
        if meeting2[1] > merged[-1][1]:
            merged.append(meeting2)
        j += 1
    return merged

'''
Finds and inputs the available times when looking at the busy schedule and
working day lists
'''
def sort_Schedule(Schedule):
    arrangedSchedule = [] 
    index = 0
    #a while a loop that checks if there is an available gap in the persons schedule 
    while index < (len(Schedule) - 1):
        if Schedule[index][1] < Schedule[index + 1][0]:
            arrangedSchedule.append([Schedule[index][1],Schedule[index + 1][0]])
            index += 1
        else:              #increment function to move through the schedule list 
            index += 1
    return arrangedSchedule   #possible avaiable times are stored adnd returned in the arrangedSchedule list 

'''
Find the avaiable times based on the duration of the meeting 
by comparing the given schedules and creates a list of the available times from person 1 and 2
back into military format 
'''
def availableTime(Schedule, duration):
    availabilities = []

    #compares if the difference between the end and start times is greater than the duration 
    for possible_availability in Schedule:
        if possible_availability[1] - possible_availability[0] >= int(duration):
            availabilities.append(possible_availability)   #if the condition is met, then this is an available time 
   
    #for every available time, the added time will be formatted to military time 
    availabilities_reconverted = []
    for plan in availabilities:
        hoursPlan = []
        for bound in plan:
            hoursPlan.append(minutesToHour(bound))
        availabilities_reconverted.append(hoursPlan)
    return availabilities_reconverted

'''Converts the string time format to its equivalent integer in minutes'''
def minuteConversion(time):
    hours, minutes = list(map(int, time.split(":")))
    return hours * 60 + minutes

'''Converts the 2d list of a time schedule into mintues'''
def listToMinutes(schedule_list):
    convertMinutes = []
    for plan in schedule_list:
        minutesPlan = []
        for bound in plan:
            minutesPlan.append(minuteConversion(bound))
        convertMinutes.append(minutesPlan)
    return convertMinutes 

'''
Converts the hours and minutes from the given avaialble time 
and converts back to string military format
'''
def minutesToHour(minutes):
    hours = minutes // 60
    mins = minutes % 60
    toString = str(hours)
    toStringMins = "0" + str(mins) if mins < 10 else str(mins)
    return toString + ":" + toStringMins

def main():
    pers1Schedule = ast.literal_eval(input("Enter schedule for person 1: "))
    pers1DailyAct = ast.literal_eval(input("Enter Daily Availability for pers 1: "))
    pers2Schedule = ast.literal_eval(input("Enter schedule for person 2: "))
    pers2DailyAct = ast.literal_eval(input("Enter Daily Availability for pers 2: "))
    duration = input("Enter duration of the proposed meeting: ")
    finalSchedule = groupSchedule(pers1Schedule, pers1DailyAct, pers2Schedule, pers2DailyAct, duration)

if __name__ == '__main__':
    main()
        