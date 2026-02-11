import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Briefcase, 
  User, 
  FileText, 
  Search, 
  LogOut,
  Home,
  Bookmark,
  MessageSquare,
} from 'lucide-react';

import JobSeekerProfile from './JobSeekerProfile'; 
import JobSearch from './JobSearch';  
import Applications from './Applications';  
import SavedJobs from './SavedJobs';    
import JobRecommendations from './JobRecommendations';
import ChatInterface from './ChatInterface';
import NotificationPanel from "../NotificationPanel";

const JobSeekerDashboard = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('home');
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5001/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      if (response.ok) {
        setUserData(data.user);
      }
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userType');
    window.location.href = '/';
  };

  const handleResumeBuilder = () => {
    navigate('/resume-builder');
  };

  const navigation = [
    { id: 'home', label: 'Home', icon: Home },
    { id: 'search', label: 'Search Jobs', icon: Search },
    { id: 'applications', label: 'My Applications', icon: Briefcase },
    { id: 'saved', label: 'Saved Jobs', icon: Bookmark },
    { id: 'resume', label: 'My Resume', icon: FileText, isExternal: true },
    { id: 'profile', label: 'Profile', icon: User },
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'home': return <JobRecommendations userData={userData} />;
      case 'search': return <JobSearch userData={userData} />;
      case 'applications': return <Applications userData={userData} />;
      case 'saved': return <SavedJobs userData={userData} />;
      case 'profile': return <JobSeekerProfile userData={userData} onUpdate={fetchUserData} />;
      case 'messages': return <ChatInterface userData={userData} />;
      default: return <JobRecommendations userData={userData} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation Bar */}
      <nav className="bg-white border-b border-gray-200 fixed w-full top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center gap-2">
              <Briefcase className="text-indigo-600" size={32} />
              <span className="text-2xl font-bold text-gray-900">JobLink</span>
            </div>

            {/* Search Bar */}
            <div className="flex-1 max-w-2xl mx-8">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="text"
                  placeholder="Search jobs, companies, skills..."
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Right Side Icons */}
            <div className="flex items-center gap-4">
              {/* Notifications - Now using NotificationPanel component */}
              <NotificationPanel />

              {/* Messages */}
              <button 
                onClick={() => setActiveTab('messages')}
                className={`p-2 rounded-lg transition-colors ${
                  activeTab === 'messages' 
                    ? 'bg-indigo-100 text-indigo-600' 
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <MessageSquare size={24} />
              </button>

              {/* Profile Dropdown */}
              <div className="flex items-center gap-2">
                <div className="w-10 h-10 bg-indigo-600 rounded-full flex items-center justify-center text-white font-semibold">
                  {userData?.email?.[0]?.toUpperCase() || 'U'}
                </div>
                <button
                  onClick={handleLogout}
                  className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg"
                  title="Logout"
                >
                  <LogOut size={20} />
                </button>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Layout */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-8">
        <div className="flex gap-6">
          {/* Left Sidebar - Navigation */}
          <aside className="w-64 flex-shrink-0">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 sticky top-20">
              <nav className="p-4 space-y-1">
                {navigation.map((item) => {
                  const Icon = item.icon;
                  
                  // Special handling for resume builder
                  if (item.id === 'resume') {
                    return (
                      <button
                        key={item.id}
                        onClick={handleResumeBuilder}
                        className="w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors text-gray-700 hover:bg-indigo-50 hover:text-indigo-600"
                      >
                        <Icon size={20} />
                        <span className="font-medium">{item.label}</span>
                      </button>
                    );
                  }
                  
                  return (
                    <button
                      key={item.id}
                      onClick={() => setActiveTab(item.id)}
                      className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                        activeTab === item.id
                          ? 'bg-indigo-50 text-indigo-600'
                          : 'text-gray-700 hover:bg-gray-50'
                      }`}
                    >
                      <Icon size={20} />
                      <span className="font-medium">{item.label}</span>
                    </button>
                  );
                })}
              </nav>
            </div>
          </aside>

          {/* Main Content Area */}
          <main className="flex-1">
            {renderContent()}
          </main>

          {/* Right Sidebar - Profile Summary & Suggestions */}
          <aside className="w-80 flex-shrink-0">
            <div className="space-y-4 sticky top-20">
              {/* Profile Completion Card */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="font-semibold text-gray-900 mb-4">Profile Strength</h3>
                <div className="mb-3">
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-indigo-600 h-2 rounded-full" style={{ width: '60%' }}></div>
                  </div>
                  <p className="text-sm text-gray-600 mt-2">60% Complete</p>
                </div>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-center gap-2 text-gray-600">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    Email verified
                  </li>
                  <li className="flex items-center gap-2 text-gray-600">
                    <div className="w-2 h-2 bg-gray-300 rounded-full"></div>
                    Add skills
                  </li>
                  <li className="flex items-center gap-2 text-gray-600">
                    <div className="w-2 h-2 bg-gray-300 rounded-full"></div>
                    Upload resume
                  </li>
                </ul>
                
                {/* Quick Resume Builder Access */}
                <button
                  onClick={handleResumeBuilder}
                  className="w-full mt-4 px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-medium hover:shadow-lg transition-all flex items-center justify-center gap-2"
                >
                  <FileText size={18} />
                  Build Resume
                </button>
              </div>

              {/* Quick Stats */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="font-semibold text-gray-900 mb-4">Quick Stats</h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Applications</span>
                    <span className="font-semibold text-gray-900">0</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Saved Jobs</span>
                    <span className="font-semibold text-gray-900">0</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Profile Views</span>
                    <span className="font-semibold text-gray-900">0</span>
                  </div>
                </div>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
};

export default JobSeekerDashboard;
