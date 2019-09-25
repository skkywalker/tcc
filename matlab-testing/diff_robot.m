clear all
close all

% Load map
map = imread('../src/test-map.png');
map_size = size(map);
%map = imresize(map, [map_size(1) map_size(2)]/2);

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
robot = differentialDriveKinematics("TrackWidth", 10, "VehicleInputs", "VehicleSpeedHeadingRate");

% Path finding
grid = binaryOccupancyMap(walls);
mapInflated = copy(grid);
inflate(mapInflated, robot.TrackWidth/2);
prm = robotics.PRM(mapInflated);
prm.NumNodes = 200;
prm.ConnectionDistance = 100;
path = findpath(prm, start, finish);

robotInitialLocation = path(1,:);
robotGoal = path(end,:);

initialOrientation = 0;

robotCurrentPose = [robotInitialLocation initialOrientation]';

controller = controllerPurePursuit;
controller.Waypoints = path;
controller.DesiredLinearVelocity = 2;
controller.MaxAngularVelocity = 4;
controller.LookaheadDistance = 0.3;
goalRadius = 5;
distanceToGoal = norm(robotInitialLocation - robotGoal);

% Initialize the simulation loop
sampleTime = 0.1;
vizRate = rateControl(1/sampleTime);

% Initialize the figure
figure

% Determine vehicle frame size to most closely represent vehicle with plotTransforms
frameSize = robot.TrackWidth/0.8;

while( distanceToGoal > goalRadius )
    
    % Compute the controller outputs, i.e., the inputs to the robot
    [v, omega] = controller(robotCurrentPose);
    
    % Get the robot's velocity using controller inputs
    vel = derivative(robot, robotCurrentPose, [v omega]);
    
    % Update the current pose
    robotCurrentPose = robotCurrentPose + vel*sampleTime;
    
    % Re-compute the distance to the goal
    distanceToGoal = norm(robotCurrentPose(1:2) - robotGoal(:));
    
    % Update the plot
    hold off
    show(grid);
    hold all
    
    % Plot path each instance so that it stays persistent while robot mesh
    % moves
    plot(path(:,1), path(:,2),"k--d")
    
    % Plot the path of the robot as a set of transforms
    plotTrVec = [robotCurrentPose(1:2); 0];
    plotRot = axang2quat([0 0 1 robotCurrentPose(3)]);
    plotTransforms(plotTrVec', plotRot, "MeshFilePath", "groundvehicle.stl", "Parent", gca, "View","2D", "FrameSize", frameSize);
    light;
    xlim([0 640])
    ylim([0 480])
    
    waitfor(vizRate);
end