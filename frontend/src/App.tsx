import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Box } from '@mui/material';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Roadmap from './pages/Roadmap';
import Demo from './pages/Demo';
import LearningEnvironment from './components/LearningEnvironment';
import Settings from './pages/Settings';

import RoadmapCreator from './components/RoadmapCreator';
import Progress from './pages/Progress';
import RoadmapDetails from './pages/RoadmapDetails';
import PrivateRoute from './components/PrivateRoute';
import Navigation from './components/Navigation';
import ErrorBoundary from './components/ErrorBoundary';
import PDFTest from './components/PDFTest';

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <AuthProvider>
          <Router>
            <Box sx={{ 
              minHeight: '100vh', 
              backgroundColor: 'background.default',
            }}>
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/demo" element={<Demo />} />
                <Route 
                  path="/dashboard" 
                  element={
                    <PrivateRoute>
                      <>
                        <Navigation />
                        <Dashboard />
                      </>
                    </PrivateRoute>
                  } 
                />
                <Route 
                  path="/roadmap" 
                  element={
                    <PrivateRoute>
                      <>
                        <Navigation />
                        <Roadmap />
                      </>
                    </PrivateRoute>
                  } 
                />
                <Route 
                  path="/learning-environment" 
                  element={
                    <PrivateRoute>
                      <>
                        <Navigation />
                        <LearningEnvironment />
                      </>
                    </PrivateRoute>
                  } 
                />

                <Route 
                  path="/roadmap/create" 
                  element={
                    <PrivateRoute>
                      <>
                        <Navigation />
                        <RoadmapCreator />
                      </>
                    </PrivateRoute>
                  } 
                />
                <Route 
                  path="/progress" 
                  element={
                    <PrivateRoute>
                      <>
                        <Navigation />
                        <Progress />
                      </>
                    </PrivateRoute>
                  } 
                />
                <Route 
                  path="/roadmap/:roadmapId" 
                  element={
                    <PrivateRoute>
                      <>
                        <Navigation />
                        <RoadmapDetails />
                      </>
                    </PrivateRoute>
                  } 
                />
                <Route 
                  path="/settings" 
                  element={
                    <PrivateRoute>
                      <>
                        <Navigation />
                        <Settings />
                      </>
                    </PrivateRoute>
                  } 
                />
                <Route 
                  path="/pdf-test" 
                  element={
                    <PrivateRoute>
                      <>
                        <Navigation />
                        <PDFTest />
                      </>
                    </PrivateRoute>
                  } 
                />
                <Route path="/" element={<Navigate to="/login" replace />} />
              </Routes>
            </Box>
          </Router>
        </AuthProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
