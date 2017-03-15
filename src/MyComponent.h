#ifndef MYCOMPONENT_H_
#define MYCOMPONENT_H_

#include <stdio.h>
#include <iostream>
#include <typeinfo>
#include <algorithm>

#include "TaylorModel.h"
#include "MyLogger.h"

class CompDependency;

class MyComponent {
  public:
    MyComponent();
    MyComponent(vector<int> vs, vector<int> tps);
    vector<int> varIndexes; //indexes to be solved in this component
    vector<int> linkVars; //linking variables, probably not needed
    vector<int> compVars; //all variable indexes in component (solve + links)
    vector<int> solveIndexes; //indexes of variables that need to be solved (wrt component variable position)
    bool isSolved;
    bool isPrepared;
    
    vector<int> tpIndexes;
    vector<int> allTMParams;
    vector<CompDependency *> dependencies;
    vector< vector<int> > compMappers;
    
    vector<MyComponent> previous;
    TaylorModelVec initSet;
    vector<HornerForm> odes;
    vector<Interval> dom;
    vector<TaylorModelVec> pipes;
    void addDependency(int linkVar, MyComponent *pComp);
    
    vector< vector<int> > previousMappers();
    vector< vector<int> > previousMappers2();
    void log();
    
    void addVar(int var);
    void prepare(TaylorModelVec tmv, const vector<HornerForm> & ode, 
       vector<Interval> domain);
    void prepareComponent(TaylorModelVec init, const vector<HornerForm> & ode, 
       vector<Interval> domain);
    void prepareVariables(TaylorModelVec tmv);
    void prepareMappers();
    void remapFlowpipes();
    void remapLastFlowpipe();
    
  private:
    void remapIVP(TaylorModelVec tmv, const vector<HornerForm> & ode, 
        vector<Interval> domain);
};

class CompDependency {
  public:
    CompDependency(int link, MyComponent *pComp);
    int linkVar;
    MyComponent *pComp;
    vector<int> mapper;
};

vector<MyComponent *> createComponents(vector< vector<int> > compIndexes, const vector<HornerForm> & ode);

MyComponent getSystemComponent(vector<MyComponent *> comps, 
    TaylorModelVec init, const vector<HornerForm> & ode, 
    vector<Interval> domain);

#endif /* MYCOMPONENT_H_ */