import React, { useState,useEffect, useCallback } from "react";
import PropTypes from 'prop-types';
import Question from './Question';
import { CSSTransitionGroup } from 'react-transition-group';
import QuestionCount from './QuestionCount';
import AnswerOption from './AnswerOption';
import {makeStyles} from "@material-ui/core/styles";


import "./StyleQuiz.css";
import PHOTOS from './api/photos';
import Masonry from "react-masonry-component";
import ImagePicker from 'react-image-picker'
import 'react-image-picker/dist/index.css'


function TypeQuiz(props) {

}

export default TypeQuiz;