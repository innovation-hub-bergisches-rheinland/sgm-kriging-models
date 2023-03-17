# load dependencies
library(SPOT)

# for reproducibility atm
seed <- 314159
set.seed(seed)

# model parameters, (re-)useable for all objectives
ctrl <- list(useLambda = T, thetaLower = 1e-4, thetaUpper = 1e3, algTheta = optimDE, budgetAlgTheta = 1000)

modelPrediction <- function(modelFit, x) {
    yEst <- predict(modelFit, matrix(x, byrow = TRUE, nrow=1))$y
    return(yEst)
}

trainCycleTime <- function(data) {
    # subselect relevant columns of training data for desired objective
    x <- as.matrix(subset(data, select = c(cooling_time, cylinder_temperature, holding_pressure_time, injection_volume_flow)))
    y <- as.matrix(subset(data, select = c(cycle_time)))
    fit <- buildKriging(x = x, y = y, control = ctrl)
    return(fit)
}

trainAvgShrinkage <- function(data) {
    # subselect relevant columns of training data for desired objective
    x <- as.matrix(subset(data, select = c(cooling_time, cylinder_temperature, holding_pressure_time, injection_volume_flow)))
    y <- as.matrix(subset(data, select = c(avg_shrinkage)))
    fit <- buildKriging(x = x, y = y, control = ctrl)
    return(fit)
}

trainMaxWarpage <- function(data) {
    # subselect relevant columns of training data for desired objective
    x <- as.matrix(subset(data, select = c(cooling_time, cylinder_temperature, holding_pressure_time, injection_volume_flow)))
    y <- as.matrix(subset(data, select = c(max_warpage)))
    fit <- buildKriging(x = x, y = y, control = ctrl)
    return(fit)
}

