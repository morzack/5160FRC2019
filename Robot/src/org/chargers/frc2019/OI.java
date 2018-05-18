package org.chargers.frc2019;

import edu.wpi.first.wpilibj.Joystick;
import edu.wpi.first.wpilibj.GenericHID.RumbleType;
import edu.wpi.first.wpilibj.buttons.Button;
import edu.wpi.first.wpilibj.buttons.JoystickButton;

/**
 * This class is the glue that binds the controls on the physical operator
 * interface to the commands and command groups that allow control of the robot.
 */
public class OI {
	// joysticks
	public static Joystick joystick0 = new Joystick(0); 	// driver 1
	public static Joystick joystick1 = new Joystick(1); 	// driver 2
	public static Joystick joystick2 = new Joystick(2); 	// sysop 1
	public static Joystick joystick3 = new Joystick(3); 	// sysop 2
	public static Joystick[] joysticks = new Joystick[]
			{joystick0, joystick1, joystick2, joystick3}; 	// array of all the joystick
	
	// toggle booleans
	public static boolean toggleSpeed = false;		// trigger on driver 1
	public static boolean toggleDirection = false;	// thumb button on driver 1
	public static boolean toggleTankDrive = false;	// button 3 on driver 1
	
	// other constants
	public static double slowSpeed = 0.5;	// slow mode
	public static double deadzone = 0.05;	// joystick deadzone
	
	// see if the number is out of the deadzone, process it
	public static double processDeadzone(double input) {
		return Math.abs(input)>=deadzone?input:0;
	}
	
	// process the input numbers, normalize and curve
	public static double processInput(double input) {
		double dead = processDeadzone(input);							// process deadzone
		double curved = dead*dead*Math.signum(dead);					// curve the input axis (input^2 while maintaining side)
		return curved*(toggleSpeed?slowSpeed:1)*(toggleDirection?-1:1);	// handle input modifiers (mostly toggles)
	}
	
	// sliders
	public static double getJoystickSlider(int stick) {
		return joysticks[stick].getRawAxis(3);
	}
	
	// get axis
	public static double getJoystickAxis(int stick, int axis) {
		return processInput(joysticks[stick].getRawAxis(axis));
	}
	public static double getJoystickX(int stick) {	// x axis
		return processInput(joysticks[stick].getX());
	}
	public static double getJoystickX2(int stick) {	// x axis stick 2
		return getJoystickAxis(stick, 4);
	}
	public static double getJoystickY(int stick) {	// y axis
		return processInput(joysticks[stick].getY());
	}
	public static double getJoystickY2(int stick) {	// y axis stick 2
		return getJoystickAxis(stick, 5);
	}
	public static double getJoystickTwist(int stick) { // twist
		return processDeadzone(joysticks[stick].getTwist());
	}
	
	// axis macros
	public static double getIntakePowerOverride(){
		return joystick2.getRawAxis(OIConstants.INTAKE_POWER_OVERRIDE_AXIS);
	}
	
	// get buttons
	public static boolean getSpeedButton() {
		return joystick0.getRawButtonPressed(OIConstants.SPEED_TOGGLE_BUTTON);
	}
	public static boolean getDirectionButton() {
		return joystick0.getRawButtonPressed(OIConstants.DIRECTION_TOGGLE_BUTTON);
	}
	public static boolean getTankDriveButton() {
		return joystick0.getRawButtonPressed(OIConstants.TANK_DRIVE_BUTTON);
	}
	public static boolean getElevatorMoveUp(){
		return joystick2.getRawButtonPressed(OIConstants.ELEVATOR_UP_BUTTON);
	}
	public static boolean getElevatorMoveDown(){
		return joystick2.getRawButtonPressed(OIConstants.ELEVATOR_DOWN_BUTTON);
	}
	public static double getIntakePower(){
		if (joystick2.getRawButton(Constants.INTAKE_POWER_POSITIVE)) {
			return 1;
		}
		else if (joystick2.getRawButton(Constants.INTAKE_POWER_NEGATIVE)) {
			return -1;
		}
		else {
			return 0;
		}
	}
}