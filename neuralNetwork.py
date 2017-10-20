import numpy
class NeuralNetwork:
    def __init__(self):
        self.weight1= numpy.random.randn()
        self.weight2 = numpy.random.randn()
        self.windSpeed = None
        self.temperature = None
        self.occur = None
        self.constant = numpy.random.randn()


    def setWeight(self,weight,number):
        if (weight == 1):
            self.weight1 = number

        else:
            self.weight2 = number

    def getWeight(self,weight):
        if(weight ==1):
            return self.weight1
        else:
            return self.weight2
    def setWindSpeed(self, speed):
        self.windSpeed = speed

    def getWindSpeed(self):
        return self.windSpeed
    def setTemperature(self,temp):
        self.temperature = temp
    def getTemperature(self):
        return self.temperature
    def setOccur(self, occur):
        self.occur = occur
    def getOccur(self):
        return  self.occur
    def setConstant(self,constant):
        self.constant = constant
    def getConstant(self):
        return self.constant
    def linearModel(self):
        result = self.getWindSpeed()*self.getWeight(1) + self.getTemperature()*self.getWeight(2)+self.getConstant()
        #print(result)
        return result
    def sigmoid(self):
        result4 = 1/(1+ numpy.exp(-self.linearModel()))
        return result4
    def Calculateerror(self):
        error = (self.sigmoid() - self.occur)**2
       # print(error)
        return error
    def sigmoid_derivative(self):
        return self.sigmoid()*(1 - self.sigmoid())
    def error_derivative(self):
        error_d = 2*(self.sigmoid()-self.occur)
        return error_d
    def weight1_derivative(self):
        return self.getWindSpeed()
    def weight2_derivative(self):
        return self.getTemperature()
    def Constant_derivative(self):
        return 1

    def derivative_error_w1(self):
        result1 = self.error_derivative()* self.sigmoid_derivative()* self.weight1_derivative()
        #print("w1"+ str(result1))
        return result1
    def derivative_error_w2(self):
        result2 = self.error_derivative()* self.sigmoid_derivative()*self.weight2_derivative()
        #print("w2" + str(result2))
        return result2
    def derivative_error_constant(self):
        result3 = self.error_derivative()* self.sigmoid_derivative()*self.Constant_derivative()
       # print("c"+ str(result3))
        return result3
    def learning_weight1(self):
        newWeight1 = self.getWeight(1) - 0.01* self.derivative_error_w1()
        self.setWeight(1,newWeight1)
        return newWeight1
    def learning_weight2(self):
        newWeight2 =  self.getWeight(2) - 0.01* self.derivative_error_w2()
        self.setWeight(2, newWeight2)
        return newWeight2
    def learning_constant(self):
        newConstant =  self.getConstant()- 0.01* self.derivative_error_constant()
        self.setConstant(newConstant)
        return newConstant