clear all
close all

omega_log = [0];
vel_log = [0];
wl = [0];
wr = [0];

% Reference to Real World
real_size = 1.2;
motor_rpm = 30;
motor_rad = motor_rpm*2*pi/60;
min_speed = 0.5;

% Load map
map = imread('../src/test3.png');
map_size = size(map);
%map = imresize(map, [map_size(1) map_size(2)]/2);
relation_real_img = map_size(2)/real_size; % pixels per meter

walls = createMask(map,100,255,0,0,0,0);
start_blob = createMask(map,0,0,100,255,0,0);
start = regionprops(start_blob,'Centroid');
start = fix(cat(1,start.Centroid));
start = [start(1) map_size(1)-start(2)];
finish_blob = createMask(map,0,0,0,0,100,255);
finish = regionprops(finish_blob,'Centroid');
finish = fix(cat(1,finish.Centroid));
finish = [finish(1) map_size(1)-finish(2)];

% Define Robot
robot = differentialDriveKinematics("TrackWidth", 0.1, "WheelRadius", 0.065/2, "VehicleInputs", "VehicleSpeedHeadingRate");

% Path finding
grid = binaryOccupancyMap(walls,relation_real_img);
mapInflated = copy(grid);
inflate(mapInflated, 0.7*robot.TrackWidth);
prm = robotics.PRM(mapInflated);
prm.NumNodes = 300;
prm.ConnectionDistance = 1;
show(prm)
path = findpath(prm, start/relation_real_img, finish/relation_real_img);

robotInitialLocation = path(1,:);
robotGoal = path(end,:);

initialOrientation = 0;

robotCurrentPose = [robotInitialLocation initialOrientation]';

controller = controllerPurePursuit;
controller.Waypoints = path;
controller.DesiredLinearVelocity = motor_rad*robot.WheelRadius;
controller.MaxAngularVelocity = 2*robot.WheelRadius*motor_rad*(1-min_speed)/robot.TrackWidth;
controller.LookaheadDistance = 0.12;
goalRadius = 0.01;
distanceToGoal = norm(robotInitialLocation - robotGoal);

% Initialize the simulation loop
sampleTime = 0.1;
vizRate = rateControl(1/sampleTime);

% Initialize the figure
figure

% Determine vehicle frame size to most closely represent vehicle with plotTransforms
frameSize = robot.TrackWidth;

while( distanceToGoal > goalRadius )
    
    % Compute the controller outputs, i.e., the inputs to the robot
    [v, omega, lookahead] = controller(robotCurrentPose);

    dist = pdist([lookahead;robotCurrentPose(1:2)']);
    
    % Get the robot's velocity using controller inputs
    vel = derivative(robot, robotCurrentPose, [v omega]);
    
    v = vel(1) + 1i*vel(2);

    if (abs(v) > motor_rad*robot.WheelRadius-abs(vel(3))*robot.TrackWidth/2)
     new_v = motor_rad*robot.WheelRadius-abs(vel(3))*robot.TrackWidth/2;
     vel(1) = new_v*cos(angle(v));
     vel(2) = new_v*sin(angle(v));
    end
    
%     v = sqrt(vel(1)^2+vel(2)^2);
%     
%     vel_log = [vel_log sqrt(vel(1)^2+vel(2)^2)];
%     omega_log = [omega_log vel(3)];
%     wl = [wl (-vel(3)*robot.TrackWidth/2+v)/robot.WheelRadius];
%     wr = [wr (vel(3)*robot.TrackWidth/2+v)/robot.WheelRadius];

    % Update the current pose
    robotCurrentPose = robotCurrentPose + vel*sampleTime;
    
    % Re-compute the distance to the goal
    distanceToGoal = norm(robotCurrentPose(1:2) - robotGoal(:));

    % Update the plot
    hold off
    show(grid);
    hold all
    plot(robotInitialLocation(1),robotInitialLocation(2), '.g', 'MarkerSize', 20, 'LineWidth', 2);
    plot(robotGoal(1), robotGoal(2), '.b', 'MarkerSize', 20, 'LineWidth', 2);
    
    % Plot lookahead point
    plot(lookahead(1),lookahead(2),'b*');

    % Plot path each instance so that it stays persistent while robot mesh
    % moves
    plot(path(:,1), path(:,2),"k--d")

    % Plot the path of the robot as a set of transforms
    plotTrVec = [robotCurrentPose(1:2); 0];
    plotRot = axang2quat([0 0 1 robotCurrentPose(3)]);
    plotTransforms(plotTrVec', plotRot, "MeshFilePath", "groundvehicle.stl", "Parent", gca, "View","2D", "FrameSize", frameSize);
    light;
    xlim([0 real_size])
    ylim([0 real_size*(map_size(1)/map_size(2))])
    
    waitfor(vizRate);
end