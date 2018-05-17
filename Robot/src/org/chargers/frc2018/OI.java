package org.chargers.frc2018;

import edu.wpi.first.wpilibj.Joystick;
import edu.wpi.first.wpilibj.GenericHID.RumbleType;
import edu.wpi.first.wpilibj.buttons.Button;
import edu.wpi.first.wpilibj.buttons.JoystickButton;

/**
 * This class is the glue that binds the controls on the physical operator
 * interface to the commands and command groups that allow control of the robot.
 */
public class OI {
	public static Joystick driver1 = new Joystick(0); //primary driver stick/controller
	public static Joystick driver2 = new Joystick(1); //second joystick for driver if in tank drive
	public static Joystick operator = new Joystick(2); //sysop
	public static Joystick safety = new Joystick(3); //used for emergency shutoff
	
	public static boolean reversed = false;
	public static boolean turnSlow = false;
	public static boolean tankDrive = false;
	public static boolean shutoff = false;
	public static boolean slowMode = false;
	
	public static double slowModifier = 0.5; //multiplied by speed when slow mode is on
	
	public static void setRumble(boolean on) {
		operator.setRumble(RumbleType.kLeftRumble, on?1:0);
		operator.setRumble(RumbleType.kRightRumble, on?1:0);
	}
	
	public static double processInput(double i) {
		return i*(slowMode?slowModifier:1)*(shutoff?0:1)*(reversed?-1:1);
	}
	
	public static double getJoystickSlider(){
		return driver1.getRawAxis(3);
	}
	
	public static boolean getReverseButton(){
		return driver1.getRawButtonPressed(2);
	}
	public static boolean getTurnSpeedButton(){
		return driver1.getRawButtonPressed(1);
	}
	
	public static double getJoystickX(){
		if(Math.abs(driver1.getX()) > 0.05){
			return processInput(driver1.getX()*driver1.getX() * Math.signum(driver1.getX()));
		}
		return 0;
	}
	
	public static double getJoystickY(){
		if(Math.abs(driver1.getY()) > 0.05){
			return processInput(driver1.getY()*driver1.getY() * Math.signum(driver1.getY()));
		}
		return 0;
	}
	
	public static double getJoystickOtherRotationX(){
		// TODO what even is this axis?
		if(Math.abs(driver1.getRawAxis(4)) > 0.05){
			return driver1.getRawAxis(4);
		}
		return 0;
	}
	
	public static double getJoystick2Y() {
		if (Math.abs(driver2.getY()) > 0.05) {
			return processInput(driver2.getY()*driver2.getY() * Math.signum(driver2.getY()));
		}
		return 0;
	}
	
	public static double getOperatorY() {
		if (Math.abs(operator.getY()) > 0.05) {
			return operator.getY()*operator.getY() * Math.signum(operator.getY());
		}
		return 0;
	}
	
	public static double getJoystickRotationX(){
		if(Math.abs(driver1.getTwist()) > 0.05){
			return driver1.getTwist();
		}
		return 0;
	}
	public static double getJoystickRotationY(){
		if(Math.abs(driver1.getRawAxis(5)) > 0.05){
			return driver1.getRawAxis(5);
		}
		return 0;
	}
	public static double getJoystickTwist(){
		if(Math.abs(driver1.getTwist()) > 0.05){
			return driver1.getTwist();
		}
		return 0;
	}
	public static boolean getElevatorMoveUp(){
		return operator.getRawButtonPressed(3);
	}
	
	public static boolean getElevatorMoveDown(){
		return operator.getRawButtonPressed(4);
	}
	
	public static double getElevatorPower(){
		if(Math.abs(operator.getY()) > 0.05){
			return operator.getY();
		}
		return 0;
	}
	public static double getIntakePowerOverride(){
		return operator.getRawAxis(5);
	}
	public static double getIntakePower(){
		if(operator.getRawButton(1)){
			return 1;
		}
		else if(operator.getRawButton(2)){
			return -1;
		}
		return 0;
	}

	public static boolean getDriveSwapButton() {
		return driver1.getRawButtonPressed(0)||driver1.getRawButtonPressed(1); //Trigger/thumb button
	}

	public static boolean getSlowModeButton() {
		return driver1.getRawButtonPressed(10); //side beast mode button
	}
	
	public static boolean getShutoffButton() {
		return safety.getRawButtonPressed(0); //"a" button
	}
}