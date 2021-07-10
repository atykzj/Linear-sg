import React from "react";
import { GridList, GridListTile, Container } from '@material-ui/core';
import { isWidthUp } from '@material-ui/core/withWidth';
import useStyles from "../styles/QuizStyles";

import { CSSTransitionGroup } from 'react-transition-group';

import { Fade } from '@material-ui/core';

function ImageLoop(props) {
    const classes = useStyles();
    const getGridListCols = () => {

        if (isWidthUp('md', props.width)) {
          return 4;
        }

        if (isWidthUp('sm', props.width)) {
          return 6;
        }

        if (isWidthUp('xs', props.width)) {
          return 12;
        }
        return 2;
    }

    return (
      <div>
            <div className={classes.container}>
                    <Container className={classes.cardGrid} maxWidth={"md"}>

                            <GridList container spacing={12} cols={getGridListCols()} cellHeight={320} >
                                 {props.PhotoList.map((tile) => (

                                        <GridListTile>

                                            <div>
                                                <img
                                                  src={tile.imageUrl}
                                                  onClick={()=> props.onPick(tile.imageUrl)}
                                              />
                                            </div>

                                        </GridListTile>

                                  ))}
                            </GridList>
                    </Container>
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

export default ImageLoop;