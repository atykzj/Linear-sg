import React, { useState } from "react";
import { Typography, AppBar, Button, Card, CardActions, CardContent, CardMedia, CssBaseline, Grid, Toolbar, Container } from '@material-ui/core';

import useStyles from "../styles/QuizStyles";
import ImageLoop from './ImageLoop';

import { Fade } from '@material-ui/core';


function Quiz(props) {
    const [image, setImage] = useState('')


    const classes = useStyles();

    function onPick(img) {
        setImage(img);
        props.onAnswerSelected(img);
    }

    return (
            <div className={classes.container}>
                <Typography variant={"h5"} style={{textAlign: "center"}}>
                    Choose your favourite image, follow your instincts
                </Typography>
                <div>
                    <ImageLoop
                      PhotoList={props.PhotoList}
                      onPick={onPick}
                    />
                </div>
            </div>

    );
}
//
// Quiz.propTypes = {
//     answer: PropTypes.string.isRequired,
//     answerOptions: PropTypes.array.isRequired,
//     counter: PropTypes.number.isRequired,
//     question: PropTypes.string.isRequired,
//     questionId: PropTypes.number.isRequired,
//     questionTotal: PropTypes.number.isRequired,
//     onAnswerSelected: PropTypes.func.isRequired
// };

export default Quiz;