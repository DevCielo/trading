import NavigationBar from "./components/NavigationBar";
import {
  BrowserRouter,
  Route,
  Routes
} from "react-router-dom";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <>
      <BrowserRouter>
        <div id='app-holder'>
          <NavigationBar />
          <div className="container">
            <Routes>
              <Route exact path="/" element={<Home />} />
              <Route exact path="/dashboard" element={<Dashboard />} />
            </Routes>
          </div>
        </div>
      </BrowserRouter>
    </>
  );
}

export default App;
