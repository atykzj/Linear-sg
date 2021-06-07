import React from "react";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";

// import Login from "./components/Login";
import Home from "./components/Home";
import QuizHome from "./components/QuizHome";
import MLPrediction from "./components/MLPrediction";
import Result from "./components/Result";
import PasswordUpdate from "./components/PasswordUpdate";

// A wrapper for <Route> that redirects to the login screen if you're not yet authenticated.
// function PrivateRoute({ isAuthenticated, children, ...rest}) {
//     return (
//       <Route
//         {...rest}
//         render={({ location }) =>
//         isAuthenticated ? (
//             children
//           ) : (
//             <Redirect
//               to={{
//                 pathname: "/login/",
//                 state: { from: location }
//               }}
//             />
//           )
//         }
//       />
//     );
// };

function Urls(props) {

// Similar to componentDidMount and componentDidUpdate:
React.useEffect(() => {
// props.setAuthenticatedIfRequired();
}, []);
    return (
        <div>
            <BrowserRouter>
                <Switch>
                    <Route exact path="/"><Home {...props}/></Route>
                    <Route exact path="/quiz"><QuizHome {...props}/></Route>
                    <Route exact path="/result/"><Result {...props}/></Route>
                    <Route exact path="/MLPrediction"><MLPrediction {...props}/></Route>

                    {/*{If authentication matters.}*/}
                    {/*<Route exact path="/login/"> <Login {...props} /></Route>*/}
                    {/*<PrivateRoute exact path="/" isAuthenticated={props.isAuthenticated}><Home {...props}/></PrivateRoute>*/}
                    {/*<PrivateRoute exact path="/update_password/" isAuthenticated={props.isAuthenticated}><PasswordUpdate {...props}/></PrivateRoute>*/}
                </Switch>
            </BrowserRouter>
        </div>
    )
};

export default Urls;