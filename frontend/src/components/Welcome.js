import React from 'react';
import { Button, Jumbotron, Container, Row } from 'react-bootstrap';

const Welcome = () => {
    return (
        <Jumbotron>
            <h1>
                <p>
                    This is simple application that retrieves photos using
                    Unsplash API. In order to start, enter any search term in
                    the input field.
                </p>
                <p>
                    <Button
                        variant="primary"
                        href="https://unsplash.com"
                        target="_blank"
                    >
                        Learn more
                    </Button>
                </p>
            </h1>
        </Jumbotron>
    );
};

export default Welcome;
