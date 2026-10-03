## Slide 1
Our system is An ML-Driven Energy Auditing and Automated Decision System for Turkish Textile Small and Medium Enterprises.
The goal of the system is to Help Turkish textile small and medium enterprises (SMEs) reduce electricity cost 
and carbon emissions, extend machine life, and preserve production throughput.

## Slide 2
Here are the mathematical formulation of our system, which can be devided into 3 parts
For the first step, our sensors take readings from each machine every 15 minutes, giving us real-time power P, 
temperature T, vibration V, and production output q. When we multiply power by time, we get the total electricity used, E.
If we divide that electricity by output, we get the energy used per item, written as EnergyPerUnit. At the same time, 
we subtract the normal baseline from current heat and vibration to see if the machine is running hotter or shaking 
more than usual.

For the second step, we bundle these numbers together—like EnergyPerUnit, temperature rise, and vibration—into a single feature group 
for our detection model. The model scores the data, and whenever the score drops below a safe cutoff line τ, the system 
triggers an alert to warn workers that something is wrong and points out what they should inspect.

## Slide 3
For the third step, which is the main planning model, the system makes choices for every machine m and every hour h. 
It uses an on-off switch y to show whether a machine runs, an output variable x for how much it makes, 
and a power variable p for how much electricity it pulls. 
The biggest combined power draw across the whole factory during any hour is the peak demand, D. In this setup, 
we balance four things together: total electricity cost C, factory peak load D, carbon emissions from grid power G, 
and machine health risk R. We put them together with priority weights λ so the math can minimize total operational cost.

Here's the constraints for the objective function
First, the total items made by each machine over the day must add up exactly to the production goal Q. 
Second, if the switch is on, production speed must stay between the machine's minimum and maximum limits. 
Third, power is not just idle power to keep the machine running, but also extra power used for each item produced. 
Finally, special machines like dyeing pumps must run three hours in a row once turned on, air systems must keep up 
with spinning-room humidity, and unhealthy machines must lower their top power or take a break.

## Slide 4
Here're the critera.
For the company, they will focus on electricity cost, energy used, machine life, and production.
For the system, it focus on the precision, recall, F1 score and False alarms

## Slide 5
Here's the workflow of the system.
First step is to take the sensor data
Then clean and transform the sensor data to what model input needs
Then use Multivariate Isolation Forest algorithm to identify abnormal pattern in a machine
Then use Explainable AI model to diagnose what reasons could be to the abnormal and find the recommended solution
Finally use mixed-interger linear programming to optimize the arragement like turning a machine on or off 
and applying how much power to specific machine to extend the machine life, achive the objective prodution 
and reduce the peak demand, carbon emission and eletricity cost

## Slide 6
Based on existing factory data, using our system can reduce peak electricity demand, 
allowing for high-power operation when electricity prices are low and low-power operation 
when electricity prices are high, thereby achieving the target output.

## Slide 7
Our system is a hybrid intelligence system that integrates AI, the ISO 10816 industry standard, 
and operational context, making it more accurate than classic AI systems.

## Slide 8
By identifying and reducing wasted electrical energy, the system can help reduce carbon emissions significantly.

## Slide 9
Because small and medium-sized enterprises (SMEs) have low profit margins, they require low-cost system deployment. 
Our system, however, requires inexpensive and simple hardware.

## Slide 10
This is our system, customized for small and medium-sized textile enterprises in Turkey. 
It helps them achieve the same output while reducing energy waste, lowering electricity costs, 
reducing carbon emissions, extending machine life, diagnosing potential machine errors, and providing recommended solutions.