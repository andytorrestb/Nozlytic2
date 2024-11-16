import matplotlib.pyplot as plt
import numpy as np

# Constants
REGRESSION_RATE_COEFFICIENT = 0.005  # Example coefficient for Eq. 16-1
OXIDIZER_FLUX_EXPONENT = 0.8        # Example exponent for Eq. 16-1
FUEL_DENSITY = 970                  # Fuel density (kg/m^3), example value
GRAIN_LENGTH = 1.0                  # Grain length (m)
INITIAL_PORT_RADIUS = 0.02          # Initial port radius (m)
MAX_PORT_RADIUS = 0.5               # Maximum port radius (m)
OXIDIZER_MASS_FLOW_RATE = 0.5       # Oxidizer mass flow rate (kg/s)
CHARACTERISTIC_VELOCITY = 1500      # c* (m/s), example value
THROAT_AREA = 0.01                  # Throat cross-sectional area (m^2)
DELTA_T = 0.01                      # Time step (s)
SIMULATION_DURATION = 10.0          # End time for simulation (s)
SINGULARITY_THRESHOLD = 0.01        # Threshold to avoid singularity near x = 0

# Functions
def calculate_regression_rate(port_radius, oxidizer_flux):
    """
    Calculate the regression rate using the appropriate equation.
    Avoid singularity near x = 0 by using a threshold.
    """
    if port_radius < SINGULARITY_THRESHOLD:
        return REGRESSION_RATE_COEFFICIENT * oxidizer_flux**OXIDIZER_FLUX_EXPONENT
    return REGRESSION_RATE_COEFFICIENT * oxidizer_flux**OXIDIZER_FLUX_EXPONENT

def calculate_fuel_flow_rate(port_radius, regression_rate):
    """
    Calculate the instantaneous fuel flow rate based on the surface area.
    """
    surface_area = 2 * np.pi * port_radius * GRAIN_LENGTH
    return FUEL_DENSITY * surface_area * regression_rate

def calculate_chamber_pressure(total_mass_flow_rate):
    """
    Calculate the chamber pressure using total mass flow rate.
    """
    return (total_mass_flow_rate * CHARACTERISTIC_VELOCITY) / THROAT_AREA

def calculate_thrust(total_mass_flow_rate):
    """
    Calculate thrust using total mass flow rate and characteristic velocity.
    """
    return total_mass_flow_rate * CHARACTERISTIC_VELOCITY

def simulate_hybrid_rocket():
    """
    Simulates the internal ballistics of a hybrid rocket motor.
    Returns simulation results for plotting.
    """
    # Initialize variables
    time = 0
    port_radius = INITIAL_PORT_RADIUS
    total_fuel_consumed = 0

    # Data storage for plots
    time_data, port_radius_data, chamber_pressure_data, thrust_data = [], [], [], []

    while time < SIMULATION_DURATION and port_radius < MAX_PORT_RADIUS:
        # Oxidizer flux
        oxidizer_flux = OXIDIZER_MASS_FLOW_RATE / (np.pi * port_radius**2)

        # Calculate regression rate
        regression_rate = calculate_regression_rate(port_radius, oxidizer_flux)

        # Update port radius
        port_radius += regression_rate * DELTA_T

        # Calculate fuel flow rate
        fuel_flow_rate = calculate_fuel_flow_rate(port_radius, regression_rate)

        # Total mass flow rate
        total_mass_flow_rate = OXIDIZER_MASS_FLOW_RATE + fuel_flow_rate

        # Calculate chamber pressure and thrust
        chamber_pressure = calculate_chamber_pressure(total_mass_flow_rate)
        thrust = calculate_thrust(total_mass_flow_rate)

        # Accumulate total fuel consumed
        total_fuel_consumed += fuel_flow_rate * DELTA_T

        # Store data for plotting
        time_data.append(time)
        port_radius_data.append(port_radius)
        chamber_pressure_data.append(chamber_pressure)
        thrust_data.append(thrust)

        # Increment time
        time += DELTA_T

    # Return results
    return time_data, port_radius_data, chamber_pressure_data, thrust_data, total_fuel_consumed, port_radius, chamber_pressure, thrust

def plot_results(time_data, port_radius_data, chamber_pressure_data, thrust_data):
    """
    Plots the simulation results for port radius, chamber pressure, and thrust.
    """
    plt.figure(figsize=(12, 8))

    # Port radius evolution
    plt.subplot(3, 1, 1)
    plt.plot(time_data, port_radius_data, label="Port Radius (m)", color='blue')
    plt.xlabel('Time (s)')
    plt.ylabel('Port Radius (m)')
    plt.title('Surface Contour Evolution')
    plt.legend()
    plt.grid(True)

    # Chamber pressure
    plt.subplot(3, 1, 2)
    plt.plot(time_data, chamber_pressure_data, label="Chamber Pressure (Pa)", color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Pressure (Pa)')
    plt.title('Chamber Pressure Evolution')
    plt.legend()
    plt.grid(True)

    # Thrust evolution
    plt.subplot(3, 1, 3)
    plt.plot(time_data, thrust_data, label="Thrust (N)", color='green')
    plt.xlabel('Time (s)')
    plt.ylabel('Thrust (N)')
    plt.title('Thrust Evolution')
    plt.legend()
    plt.grid(True)

    # Adjust layout and show
    plt.tight_layout()
    plt.show()

def main():
    """
    Main function to run the hybrid rocket simulation and plot results.
    """
    # Run simulation
    results = simulate_hybrid_rocket()
    time_data, port_radius_data, chamber_pressure_data, thrust_data = results[:4]
    total_fuel_consumed, final_port_radius, final_chamber_pressure, final_thrust = results[4:]

    # Print final results
    print(f"Simulation completed. Total fuel consumed: {total_fuel_consumed:.2f} kg")
    print(f"Final port radius: {final_port_radius:.3f} m")
    print(f"Final chamber pressure: {final_chamber_pressure:.2f} Pa")
    print(f"Final thrust: {final_thrust:.2f} N")

    # Plot results
    plot_results(time_data, port_radius_data, chamber_pressure_data, thrust_data)

# Run the program
if __name__ == "__main__":
    main()
