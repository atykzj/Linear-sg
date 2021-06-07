import React from 'react';
import PropTypes from 'prop-types';
import { CSSTransitionGroup } from 'react-transition-group';
import {Link} from "react-router-dom";
import {Button} from "@material-ui/core";

function Result(props) {
  return (
    <CSSTransitionGroup
      className="container result"
      component="div"
      transitionName="fade"
      transitionEnterTimeout={800}
      transitionLeaveTimeout={500}
      transitionAppear
      transitionAppearTimeout={500}
    >
      <div>
        Returned results values: <strong>{props.quizResult}</strong>!
      </div>
      <div>
          <Link to="/">
              <Button variant="contained" color="primary">
                  Back to Home
              </Button>
          </Link>
      </div>
    </CSSTransitionGroup>
  );
}

Result.propTypes = {
  quizResult: PropTypes.string.isRequired
};

export default Result;