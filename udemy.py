import math

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def r(num):#just to round up the numbers to 14 decimal places
    return round(num, 14)

def printResult(real, imaginary):
    if imaginary < 0:
        return str(r(real)) + " - " + str(r(imaginary)) + "i"
    elif imaginary == 0:
        return r(real)
    elif real == 0:
        return str(r(imaginary)) + "i"
    return str(r(real)) + " + " + str(r(imaginary)) + "i"

acceptableTolerance = eval(input("Enter the acceptable tolerance : "))
angleInDegrees = eval(input("Enter an angle in degrees : "))

angleInRadian = (math.pi * angleInDegrees) / 180.0

print("\nAngle in radian = ", angleInRadian, ", angle in degrees = ", angleInDegrees)
actualRealPart = math.cos(angleInRadian)
actualImaginaryPart = math.sin(angleInRadian)

computedTolerance = acceptableTolerance - 1 #this logic keeps the loop until the main condition is satisfied
n = 0
calcRealPart = 0
calcImaginaryPart = 0
NumberOfTimesForReal = 1
NumberOfTermsForImaginary = 1
diffInReal = 0
diffInImaginary = 0
while True:
    calcRealPart += (pow(-1, n) * pow(angleInRadian, 2 * n)) / factorial(2 * n)
    calcImaginaryPart += (pow(-1, n) * pow(angleInRadian, 2 * n + 1)) / factorial(2 * n + 1)
    diffInReal = calcRealPart - actualRealPart
    diffInImaginary = calcImaginaryPart - actualImaginaryPart

    if abs(diffInReal) > acceptableTolerance:
        NumberOfTimesForReal += 1
    if abs(diffInImaginary) > acceptableTolerance:
        NumberOfTermsForImaginary += 1

    if abs(diffInReal) <= acceptableTolerance and abs(diffInImaginary) <= acceptableTolerance:
        break
    n += 1

print("\nPython value for e^ix(", angleInDegrees, ") = ", printResult(actualRealPart, actualImaginaryPart))
print("\nApproximate value for e^ix(", angleInDegrees, ") = ", printResult(calcRealPart, calcImaginaryPart))
print("\nNumber of terms for the real part is ", NumberOfTimesForReal, ", Number of terms for the imaginary part is ", NumberOfTermsForImaginary)
print("\nTolerance = ", printResult(diffInReal, diffInImaginary))