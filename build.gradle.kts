plugins {
    kotlin("jvm") version "1.6.10"
}

repositories {
    mavenCentral()
}

tasks {
    sourceSets {
        main {
            java.srcDirs("2015", "2020", "2021")
        }
    }
}
dependencies {
    implementation(kotlin("script-runtime"))
}
